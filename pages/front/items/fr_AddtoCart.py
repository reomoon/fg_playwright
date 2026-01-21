from playwright.sync_api import Page
from core.page_wrapper import HighlightPageWrapper

def add_item_to_cart(page: Page):
    # 1) 활성화(클릭 가능) + 보이는 입력칸이 나타날 때까지 대기
    page.wait_for_selector(
        "input.txtPkQty:enabled:visible, input.jsOpenPackEachQty:enabled:visible",
        timeout=15000
    )

    # 2) 입력 가능한 수량 필드 수집 (비활성 제외)
    prepack_fields = page.locator("input.txtPkQty:enabled:visible")
    openpack_fields = page.locator("input.jsOpenPackEachQty:enabled:visible")
    success = False

    # 3) Prepack(박스 단위) 먼저 입력 시도
    prepack_count = prepack_fields.count()
    for i in range(prepack_count):
        field = prepack_fields.nth(i)
        try:
            field.scroll_into_view_if_needed()
            field.fill("5")
            success = True
            print(f"🅿 Prepack 수량 입력 성공 (index={i})")
            break
        except Exception as e:
            print(f"❌ Prepack 입력 실패 (index={i}): {e}")

    # 4) Prepack이 없거나 실패하면 Openpack(개별 단위) 입력 시도
    if not success:
        openpack_count = openpack_fields.count()
        for i in range(openpack_count):
            field = openpack_fields.nth(i)
            try:
                field.scroll_into_view_if_needed()
                field.click(timeout=1000)
                field.fill("5")
                success = True
                print(f"🅿 Openpack 수량 입력 성공 (index={i})")
                break
            except Exception as e:
                print(f"❌ Openpack 입력 실패 (index={i}): {e}")

    # 5) 모든 입력 시도가 실패했을 경우 예외 발생
    if not success:
        raise Exception("❌ 입력 가능한 수량 필드를 찾지 못했습니다.")

    # 6) 장바구니 버튼 클릭 후 AddCart 응답 잡기
    def is_addcart_response(response):
        return (
            "/Cart/AddCart" in response.url
            and response.request.method == "POST"
        )

    with page.expect_response(is_addcart_response, timeout=15000) as resp_info:
        page.click("button.addCart")

    resp = resp_info.value

    # 7) HTTP 상태 체크
    if resp.status != 200:
        print(f"❌ 장바구니 실패 (HTTP {resp.status})")
        return False, f"HTTP {resp.status}"

    # 8) JSON success 체크 (여기가 핵심)
    try:
        result = resp.json()
    except Exception as e:
        print(f"❌ 장바구니 실패 (JSON 파싱 실패): {e}")
        return False, "JSON 파싱 실패"

    api_success = result.get("success", False)
    message = result.get("message") or result.get("reason") or "장바구니 API 실패(사유 없음)"

    if api_success is True:
        print(f"🅿 장바구니 담기 성공 (success=True) 응답: {result}")
        return True, message
    else:
        print(f"❌ 장바구니 담기 실패 (success=False) 응답: {result}")
        return False, message

def run_add_to_cart_flow(page: Page, vendor_name: str = "Allium"):
    # 1) 검색창 대기
    search_input = page.locator('#lb_sch')
    search_input.wait_for(state="visible", timeout=15000)
    print("☑ #lb_sch found (검색창)")

    search_input.click()
    search_input.press("Control+A")
    search_input.press("Delete")
    search_input.type(vendor_name, delay=80)

    # 2) 자동완성 Vendor 클릭
    vendor_suggestion = page.locator(
        'div.autoSuggestBox.searchNew ._resultBox li.srch[data-nclick-name="site.keyword.vsuggest"]'
    ).filter(has_text=vendor_name)

    vendor_suggestion.wait_for(state="visible", timeout=15000)
    print(f"☑ 자동완성 'Vendor > {vendor_name}' 항목 노출")

    with page.expect_navigation():
        vendor_suggestion.first.click()

    page.wait_for_load_state("networkidle")

    # 3) All Items 첫 상품 클릭
    all_items_first_thumb = page.locator(
        'ul.lst_pdt li.heapData[data-heap-component-name="All Items"] '
        'div.pic a[href^="/Item/"]'
    ).first

    all_items_first_title = page.locator(
        'ul.lst_pdt li.heapData[data-heap-component-name="All Items"] '
        'div.info p a.item[href^="/Item/"]'
    ).first

    if all_items_first_thumb.count() > 0:
        all_items_first_thumb.wait_for(state="visible", timeout=15000)
        target_link = all_items_first_thumb
        print("☑ All Items 첫 썸네일 링크 감지")
    else:
        all_items_first_title.wait_for(state="visible", timeout=15000)
        target_link = all_items_first_title
        print("☑ All Items 첫 타이틀 링크(폴백) 감지")

    with page.expect_navigation():
        target_link.click()

    page.wait_for_url("**/Item/**", timeout=15000)
    page.wait_for_load_state("networkidle")
    print("🅿 아이템 디테일 페이지 이동 성공")

    # 4) 장바구니 담기 (API success까지 검증됨)
    success, message = add_item_to_cart(page)
    if not success:
        raise Exception(f"❌ 장바구니 담기 실패: {message}")

    # 5) Cart 페이지에서 실제 존재 검증
    product_id = page.url.split('/')[-1].split('?')[0]
    print(f"☑ 추출한 Product ID: {product_id}")

    page.goto("https://beta-www.fashiongo.net/cart")
    page.wait_for_load_state("networkidle")

    selector = f".goods-detail[id='{product_id}']"
    item_in_cart = page.locator(selector)

    if item_in_cart.count() <= 0:
        raise Exception(f"❌ 장바구니에 Product ID {product_id} 없음")

    print("🅿 장바구니 전체 플로우 검증 성공")