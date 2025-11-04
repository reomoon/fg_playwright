from playwright.sync_api import Page, expect
import re

# ✅ 1) productid.txt에서 마지막 productId 읽기
def get_last_product_id(filepath="productid.txt"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.read().strip().splitlines()
            if not lines:
                raise ValueError("파일은 있지만 내용이 비어 있습니다.")
            last_id = lines[-1].strip()
            print(f"🅿 [마지막 상품ID 읽기 성공] {last_id}")
            return last_id
    except FileNotFoundError:
        print("❌ [productid.txt 없음] 먼저 상품 생성 테스트를 실행하세요.")
        return None
    except Exception as e:
        print(f"❌ [상품ID 읽기 실패] {e}")
        return None


# ✅ 2) 벤더 프로모션 적용 (벤더ID=16502, 첫 번째 프로모션 Apply 클릭)
def apply_vendor_promotion(page: Page):
    # 2-1) 생성된 상품 ID 확인 및 디테일 이동
    product_id = get_last_product_id()
    if not product_id:
        raise Exception("생성한 상품 ID를 찾을 수 없어 프로모션 테스트를 중단합니다.")

    item_url = f"https://beta-www.fashiongo.net/item/{product_id}"
    page.goto(item_url)
    page.wait_for_load_state("domcontentloaded")
    print(f"🅿 아이템 디테일 이동: {item_url}")

    # 2-2) 수량 입력 → 장바구니 담기
    try:
        page.wait_for_selector("input.txtPkQty", timeout=10000)
        print("☑ input.txtPkQty found (1개)")
        qty_input = page.locator("input.txtPkQty").first
        qty_input.fill("4")
        print("☑ Prepack 수량 입력 성공 (4)")
    except Exception as e:
        page.screenshot(path="debug_qty_not_found.png")
        raise Exception("Prepack 수량 입력 필드를 찾지 못했습니다.") from e

    try:
        page.wait_for_selector("button.addCart", timeout=10000)
        print("☑ button.addCart found (1개)")
        page.locator("button.addCart").first.click()
        page.wait_for_timeout(1500)
        print("☑ 장바구니 담기 버튼 클릭 완료")
    except Exception as e:
        page.screenshot(path="debug_addcart_fail.png")
        raise Exception("장바구니 담기 버튼 클릭 실패") from e

    # 2-3) 장바구니 페이지 이동
    page.goto("https://beta-www.fashiongo.net/cart")
    print("🅿 장바구니 페이지 이동")

    # 2-4) Vendor Promotion 버튼(벤더ID=16502) 클릭 + cartItemId 추출
    try:
        page.wait_for_selector("button.btn-vendor", timeout=10000)
        btn_sel = 'button.btn-vendor[data-nclick-extra*="vid=16502"]'
        expect(page.locator(btn_sel)).to_have_count(1, timeout=3000)
        print("☑ button.btn-vendor[data-nclick-extra*=\"vid=16502\"] found (1개)")

        vendor_btn = page.locator(btn_sel).first
        vendor_btn.scroll_into_view_if_needed()

        extra_data = vendor_btn.get_attribute("data-nclick-extra") or ""
        # 예: data-nclick-extra="..., rid:566735, vid=16502, ..."
        m = re.search(r"rid:(\d+)", extra_data)
        if not m:
            raise Exception("cartItemId(rid) 추출 실패")
        cart_item_id = m.group(1)
        print(f"🅿 cartItemId 추출: {cart_item_id}")

        vendor_btn.click()
        print("🅿 Vendor Promotions 버튼 클릭 완료 (vid=16502)")

        # 프로모션 레이어/목록 로딩 대기
        page.wait_for_selector(".coupon-area .coupon-item", timeout=10000)
        page.wait_for_selector(".coupon-area .coupon-item .btn-coupon-apply", timeout=10000)
        print("☑ 프로모션 목록 로딩 완료")
    except Exception as e:
        page.screenshot(path="debug_vendor_btn_fail.png")
        raise Exception("Vendor Promotions 버튼 처리 실패 (vid=16502)") from e

    # 2-5) 첫 번째 프로모션 Apply 클릭 (+ 이미 적용되어 있으면 취소 후 재적용)
    try:
        first_item = page.locator(".coupon-area .coupon-item").first
        expect(first_item).to_be_visible(timeout=5000)

        # 이미 Applied 표시가 보이면 취소 후 재적용
        try:
            if first_item.locator(".checked-coupon-apply").is_visible():
                if first_item.locator(".btn-coupon-cancel").count() > 0:
                    first_item.locator(".btn-coupon-cancel").click()
                    page.wait_for_timeout(400)
                    print("☑ 기존 적용 취소 후 재적용 진행")
        except Exception:
            # 표시가 없거나 is_visible 타이밍 이슈는 무시
            pass

        apply_btn = first_item.locator(".btn-coupon-apply").first
        expect(apply_btn).to_be_visible(timeout=5000)

        # 응답 감시: 환경별 엔드포인트 차이를 고려해 OR 다중 조건
        def _is_apply_resp(res):
            url_ok = (
                f"/CartItem/{cart_item_id}" in res.url
                or "/Cart/Apply" in res.url
                or "/Cart/ApplyPromotion" in res.url
                or "/Cart/ApplyDiscount" in res.url
            )
            return url_ok and res.request.method == "POST"

        with page.expect_response(_is_apply_resp, timeout=10000) as resp_info:
            apply_btn.click()

        resp = resp_info.value
        print(f"🅿 프로모션 적용 API 응답 상태코드: {resp.status}")
        print(f"☑ 응답 URL: {resp.url}")
        if resp.status != 200:
            raise Exception(f"응답 상태 코드가 200이 아닙니다: {resp.status}")

        print("🅿 200 응답 확인: 첫 번째 프로모션 적용 성공")
    except Exception as e:
        page.screenshot(path="debug_apply_promotion_fail.png")
        raise Exception("프로모션 적용 중 오류 발생") from e