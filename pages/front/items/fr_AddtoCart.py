from playwright.sync_api import Page
from core.page_wrapper import HighlightPageWrapper

def add_item_to_cart(page: Page):
    # 활성화된 입력 필드만 기다림 (disabled 제외)
    page.wait_for_selector("input.txtPkQty:enabled, input.jsOpenPackEachQty:enabled", timeout=10000)

    prepack_fields = page.locator("input.txtPkQty")
    openpack_fields = page.locator("input.jsOpenPackEachQty")
    success = False

    # Prepack 처리
    prepack_count = prepack_fields.count()
    for i in range(prepack_count):
        field = prepack_fields.nth(i)
        if field.is_enabled():
            try:
                field.fill("10")
                success = True
                print(f"Prepack 입력 성공 (index={i})")
                break
            except Exception as e:
                print(f"Prepack 입력 실패 (index={i}): {e}")
        else:
            print(f"Prepack 입력 불가 (index={i}) - disabled")

    # Openpack 처리 (Prepack 실패 시)
    if not success:
        openpack_count = openpack_fields.count()
        for i in range(openpack_count):
            field = openpack_fields.nth(i)
            if field.is_enabled():
                try:
                    field.click(timeout=1000)
                    field.fill("10")
                    success = True
                    print(f"Openpack 입력 성공 (index={i})")
                    break
                except Exception as e:
                    print(f"Openpack 입력 실패 (index={i}): {e}")
            else:
                print(f"Openpack 입력 불가 (index={i}) - disabled")

    # 입력 실패 시 예외 발생
    if not success:
        raise Exception("입력 가능한 수량 필드를 찾지 못했습니다.")

    # 장바구니 버튼 클릭 및 API 응답 확인
    def is_addcart_response(response):
        return (
            "/Cart/AddCart" in response.url
            and response.request.method == "POST"
            and response.status == 200
        )

    with page.expect_response(is_addcart_response, timeout=10000):
        page.click("button.addCart")

    print("장바구니 담기 성공 (API 200 응답 확인됨)")