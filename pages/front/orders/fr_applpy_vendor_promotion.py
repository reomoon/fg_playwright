from playwright.sync_api import Page, expect
import re

def apply_vendor_promotion(page: Page):
    # 1. 아이템 디테일 페이지로 이동
    page.goto("https://www.fashiongo.net/Item/21748958")
    page.wait_for_load_state("domcontentloaded")

    # 2. qty 입력필드에 4 입력
    try:
        page.wait_for_selector("input.txtPkQty", timeout=10000)
        qty_input = page.locator("input.txtPkQty").first
        qty_input.fill("4")
        print("Prepack 수량 입력 성공")
    except Exception as e:
        page.screenshot(path="debug_qty_not_found.png")
        raise Exception("Prepack 수량 입력 필드를 찾지 못했습니다.") from e

    # 3. 쇼핑백에 담기 버튼 클릭
    add_to_bag_btn = page.locator("button.addCart")
    add_to_bag_btn.click()

    # 장바구니 이동을 위한 페이지 로딩 대기
    page.wait_for_timeout(3000)  # 네트워크 응답이 느릴 수 있어서 약간 대기

    # 4. 쇼핑백 페이지로 이동
    page.goto("https://www.fashiongo.net/cart")

    # 5. Vendor Promotion 버튼 클릭 및 cartItemId 추출
    try:
        page.wait_for_selector("button.btn-vendor", timeout=10000)
        vendor_btn = page.locator('button.btn-vendor[data-nclick-extra*="vid=2289"]').first
        vendor_btn.scroll_into_view_if_needed()

        extra_data = vendor_btn.get_attribute("data-nclick-extra")
        match = re.search(r"rid:(\d+)", extra_data)
        if not match:
            raise Exception("cartItemId 추출 실패")
        cart_item_id = match.group(1)
        print("cartItemId 추출:", cart_item_id)

        vendor_btn.click()
        print("Vendor Promotions 버튼 클릭 완료")
    except Exception:
        page.screenshot(path="debug_vendor_btn_fail.png")
        raise Exception("Vendor Promotions 버튼 처리 실패")

    try:
        promo = page.locator('div.coupon-item[discountid="65358"]')
        expect(promo).to_be_visible(timeout=5000)
        promo.scroll_into_view_if_needed()

        apply_btn = promo.locator("button.btn-coupon-apply")
        expect(apply_btn).to_be_visible(timeout=5000)

        with page.expect_response(
            lambda res: f"/CartItem/{cart_item_id}" in res.url and res.request.method == "POST",
            timeout=10000
        ) as resp_info:
            apply_btn.click()

        response = resp_info.value
        print("프로모션 적용 API 응답 상태코드:", response.status)
        print("응답 URL:", response.url)

        if response.status == 200:
            print("200 응답 확인: 프로모션 적용 성공")
        else:
            raise Exception(f"응답 상태 코드가 200이 아닙니다: {response.status}")

    except Exception as e:
        page.screenshot(path="debug_apply_promotion_fail.png")
        raise Exception("프로모션 적용 중 오류 발생") from e