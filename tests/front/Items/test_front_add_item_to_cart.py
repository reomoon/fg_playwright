from playwright.sync_api import Page, expect
from pages.front.items.fr_AddtoCart import add_item_to_cart
from tests.front.login.test_front_login_fixture import front_login_fixture

def test_add_item_to_cart(front_login_fixture):
    page = front_login_fixture  # 로그인된 페이지 사용

    search_input = page.locator('#lb_sch')
    search_input.wait_for(state="visible", timeout=15000)
    print("☑ #lb_sch found (검색창)")

    search_input.click()
    # (선택) 기존 값이 남아있을 수 있으니 비우기
    search_input.press("Control+A")
    search_input.press("Delete")

    # 한 글자씩 타이핑 (자동완성 자연 노출 유도)
    search_input.type("Allium", delay=80)  # ms 단위 지연(원하면 40~120 사이로 조절 가능)

    vendor_suggestion = page.locator(
        'div.autoSuggestBox.searchNew ._resultBox li.srch[data-nclick-name="site.keyword.vsuggest"]'
    ).filter(has_text="Allium")
    vendor_suggestion.wait_for(state="visible", timeout=15000)
    print("☑ 자동완성 'Vendor > Allium' 항목 노출") 

    with page.expect_navigation():
        vendor_suggestion.first.click()

    # 3) 벤더 홈 도착 확인
    page.wait_for_load_state("networkidle")
    # expect(page).to_have_url(lambda url: "/Vendor" in url or "/vendor" in url)
    # print("🅿 벤더 홈 이동 성공")

    # 4) All Items 리스트에서 첫 번째 아이템 타일 클릭 → 디테일 페이지
    # li.heapData[data-heap-component-name="All Items"] 내부의 썸네일 링크 우선 시도
    all_items_first_thumb = page.locator(
        'ul.lst_pdt li.heapData[data-heap-component-name="All Items"] '
        'div.pic a[href^="/Item/"]'
    ).first

    # 폴백: 혹시 썸네일 링크가 렌더 전이면 타이틀 링크로 재시도
    all_items_first_title = page.locator(
        'ul.lst_pdt li.heapData[data-heap-component-name="All Items"] '
        'div.info p a.item[href^="/Item/"]'
    ).first

    # 첫 요소 대기(썸네일 우선, 없으면 타이틀)
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

    # 5) 디테일 페이지 로딩 완료
    page.wait_for_url("**/Item/**", timeout=15000)
    page.wait_for_load_state("networkidle")
    print("🅿 아이템 디테일 페이지 이동 성공")

    # 6) 장바구니 담기 (내부에서 입력/대기 처리)
    add_item_to_cart(page)

    # 7) 현재 상세페이지의 URL에서 상품 ID 추출
    product_id = page.url.split('/')[-1].split('?')[0]
    print("☑ 추출한 Product ID:", product_id)

    # 8) 장바구니 페이지로 이동
    page.goto("https://beta-www.fashiongo.net/cart")
    page.wait_for_load_state("networkidle")

    # 9) 장바구니 내 해당 상품 존재 확인
    selector = f".goods-detail[id='{product_id}']"
    item_in_cart = page.locator(selector)

    # 10) 검증
    assert item_in_cart.count() > 0, f"장바구니에 Product ID {product_id}가 존재하지 않음"
    print("🅿 장바구니 검증 성공")