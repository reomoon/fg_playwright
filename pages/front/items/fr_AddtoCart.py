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
            field.fill("1")
            success = True
            print(f"Prepack 수량 입력 성공 (index={i})")
            break
        except Exception as e:
            print(f"Prepack 입력 실패 (index={i}): {e}")

    # 4) Prepack이 없거나 실패하면 Openpack(개별 단위) 입력 시도
    if not success:
        openpack_count = openpack_fields.count()
        for i in range(openpack_count):
            field = openpack_fields.nth(i)
            try:
                field.scroll_into_view_if_needed()
                field.click(timeout=1000)
                field.fill("1")
                success = True
                print(f"Openpack 수량 입력 성공 (index={i})")
                break
            except Exception as e:
                print(f"Openpack 입력 실패 (index={i}): {e}")

    # 5) 모든 입력 시도가 실패했을 경우 예외 발생
    if not success:
        raise Exception("입력 가능한 수량 필드를 찾지 못했습니다.")

    # 6) 장바구니 버튼 클릭 후 API 응답(200) 확인
    def is_addcart_response(response):
        return (
            "/Cart/AddCart" in response.url
            and response.request.method == "POST"
            and response.status == 200
        )

    with page.expect_response(is_addcart_response, timeout=15000):
        page.click("button.addCart")

    print("장바구니 담기 성공 (API 200 응답 확인됨)")