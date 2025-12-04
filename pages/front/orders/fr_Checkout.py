from playwright.sync_api import Page
from pathlib import Path


def capture_screenshot(page: Page, name: str):
    path = Path(f"screenshots/{name}.png")
    path.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=path)
    print(f"🗙 [스크린샷 저장] {path}")


def click_button_safe(page: Page, selector: str, step_name: str, timeout: int = 5000) -> bool:
    """
    버튼 클릭을 안전하게 시도하는 헬퍼 함수.
    - 성공: True 반환
    - 실패: 스크린샷 남기고 False 반환
    """
    print(f"☑ [{step_name}] 버튼 찾기 시도: {selector}")
    try:
        page.wait_for_selector(selector, timeout=timeout)
        button = page.locator(selector)
        button.click()
        print(f"🅿 [{step_name}] 버튼 클릭 성공")
        return True
    except Exception as e:
        print(f"❌ [{step_name}] 버튼 클릭 실패 - {e}")
        capture_screenshot(page, f"fail_{step_name.replace(' ', '_')}")
        return False


def checkout_flow(page: Page):
    """
    반환값: (success: bool, message: str)

    success == False 인 경우, message 에
    'STEPx - 어떤 작업에서 어떤 이유로 실패했는지' 를 담아서 반환.
    """

    # ─────────────────────────────
    # STEP 1. Cart 페이지 진입
    # ─────────────────────────────
    step = "STEP1 - Cart 페이지 이동"
    print(f"☑ {step}")
    try:
        page.goto("https://beta-www.fashiongo.net/cart")
        page.wait_for_load_state("load")
        print(f"🅿 {step} 완료")
    except Exception as e:
        msg = f"{step} 실패: 페이지 이동 중 예외 발생 ({e})"
        print(f"❌ {msg}")
        capture_screenshot(page, "fail_step1_cart_goto")
        return False, msg

    # ─────────────────────────────
    # STEP 2. Checkout this vendor only 버튼 클릭
    # ─────────────────────────────
    step = "STEP2 - Checkout Vendor Only 버튼 클릭"
    order_id = "16502"  # 필요 시 파라미터로 뺄 수 있음
    selector = f'#order{order_id} button.btn-checkoutVendor'

    if not click_button_safe(page, selector, step_name=step):
        msg = f"{step} 실패: 버튼 클릭 불가"
        return False, msg

    # ─────────────────────────────
    # STEP 3. 모달(Pre-checkout) 처리
    # ─────────────────────────────
    step = "STEP3 - 모달 확인 및 Continue To Checkout 클릭"
    print(f"☑ {step}")
    modal_detected = False
    try:
        for _ in range(30):
            modal_visible = page.evaluate(
                """() => {
                    const modal = document.querySelector('div.modal_beforeCheckout');
                    return modal && window.getComputedStyle(modal).display === 'block';
                }"""
            )
            if modal_visible:
                print("🅿 [모달 감지] modal_beforeCheckout display: block")
                modal_detected = True
                break
            page.wait_for_timeout(100)
    except Exception as e:
        # 🔴 여기부터 수정 포인트
        error_text = str(e)
        if "Execution context was destroyed" in error_text:
            # 네비게이션 때문에 컨텍스트가 사라진 경우 → 모달 없이 다음 단계 진행
            print(f"☑ {step}: 네비게이션 감지, 모달 없이 진행 (에러 무시) - {e}")
            modal_detected = False
        else:
            # 진짜 이상한 에러는 기존처럼 실패 처리
            msg = f"{step} 실패: 모달 표시 여부 체크 중 예외 발생 ({e})"
            print(f"❌ {msg}")
            capture_screenshot(page, "fail_step3_modal_check")
            return False, msg

    if modal_detected:
        try:
            modal_button = page.locator('div.modal_beforeCheckout button.btn-sure')
            if modal_button.is_visible():
                modal_button.click()
                print("🅿 [모달] Continue To Checkout 버튼 클릭 성공")
            else:
                msg = f"{step} 실패: 모달 버튼이 visible 하지 않음"
                print(f"❌ {msg}")
                capture_screenshot(page, "fail_step3_modal_button_not_visible")
                return False, msg
        except Exception as e:
            msg = f"{step} 실패: 모달 버튼 클릭 중 예외 발생 ({e})"
            print(f"❌ {msg}")
            capture_screenshot(page, "fail_step3_modal_click_exception")
            return False, msg
    else:
        print("☑ [모달 없음] 모달 없이 다음 단계 진행")

    # ─────────────────────────────
    # STEP 4. Checkout Step1 → Step2 (Save & Continue)
    # ─────────────────────────────
    step = "STEP4 - Save & Continue (Step1) 버튼 클릭"
    page.wait_for_load_state("load")
    try:
        page.wait_for_selector("button.btn-goToPayment", timeout=15000)
    except Exception as e:
        msg = f"{step} 실패: 버튼이 화면에 나타나지 않음 ({e})"
        print(f"❌ {msg}")
        capture_screenshot(page, "fail_step4_button_not_found")
        return False, msg

    if not click_button_safe(page, "button.btn-goToPayment", step_name=step):
        msg = f"{step} 실패: 버튼 클릭 실패"
        return False, msg

    # ─────────────────────────────
    # STEP 5. Checkout Step2 → Step3 (Save & Continue)
    # ─────────────────────────────
    step = "STEP5 - Save & Continue (Step2) 버튼 클릭"
    page.wait_for_load_state("load")
    if not click_button_safe(page, "button.btn-goToReview", step_name=step):
        msg = f"{step} 실패: 버튼 클릭 실패"
        return False, msg

    # ─────────────────────────────
    # STEP 6. Checkout Step3 → Submit Order
    # ─────────────────────────────
    step = "STEP6 - Submit Order 버튼 클릭"
    page.wait_for_load_state("load")
    if not click_button_safe(page, "button.btn-checkout", step_name=step):
        msg = f"{step} 실패: 버튼 클릭 실패"
        return False, msg

    # ─────────────────────────────
    # STEP 7. Submit 이후 Order No 추출
    # ─────────────────────────────
    step = "STEP7 - Order No 추출"
    print(f"☑ {step}")
    page.wait_for_load_state("load")
    try:
        page.wait_for_selector("a.link-order", timeout=10000)
        order_no = page.locator("a.link-order").inner_text().strip()
        print(f"🅿 {step} 완료 - 추출된 오더번호: {order_no}")
    except Exception as e:
        msg = f"{step} 실패: Order No 추출 중 예외 발생 ({e})"
        print(f"❌ {msg}")
        capture_screenshot(page, "fail_step7_order_no")
        return False, msg

    # ─────────────────────────────
    # STEP 8. Order History 에서 방금 주문한 Order No 확인
    # ─────────────────────────────
    step = "STEP8 - Order History 에서 Order No 확인"
    print(f"☑ {step}")
    page.goto("https://beta-www.fashiongo.net/MyAccount/OrderHistory")
    try:
        found = False
        for _ in range(50):
            order_sn_locator = page.locator("span.order-sn").filter(has_text=order_no)
            if order_sn_locator.first.is_visible():
                print(f"🅿 {step} 완료 - Order History 에서 {order_no} 발견")
                found = True
                break
            page.wait_for_timeout(200)

        if not found:
            msg = f"{step} 실패: Order History 에서 {order_no} 를 찾지 못함"
            print(f"❌ {msg}")
            capture_screenshot(page, "fail_step8_order_history")
            return False, msg

    except Exception as e:
        msg = f"{step} 실패: Order History 페이지 로딩/조회 중 예외 발생 ({e})"
        print(f"❌ {msg}")
        capture_screenshot(page, "fail_step8_order_history_exception")
        return False, msg

    # ─────────────────────────────
    # STEP 9. Order Detail 페이지 진입 및 h1에서 Order No 검증
    # ─────────────────────────────
    step = "STEP9 - Order Detail 페이지에서 Order No 확인"
    print(f"☑ {step}")
    try:
        order_sn_locator.first.click()
        page.wait_for_load_state("networkidle")

        page.wait_for_selector("div.tit_bx h1", timeout=10000)
        h1_text = page.locator("div.tit_bx h1").inner_text().strip()

        if order_no in h1_text:
            print(f"🅿 {step} 완료 - 디테일 페이지 h1에 {order_no} 표시 확인")
            print("🅿 체크아웃 전체 플로우 성공")
            return True, "체크아웃 플로우 전체 성공"
        else:
            msg = f"{step} 실패: 디테일 페이지 h1 텍스트에 {order_no} 미포함"
            print(f"❌ {msg}")
            capture_screenshot(page, "fail_step9_detail_h1_mismatch")
            return False, msg

    except Exception as e:
        msg = f"{step} 실패: 디테일 페이지 이동/검증 중 예외 발생 ({e})"
        print(f"❌ {msg}")
        capture_screenshot(page, "fail_step9_detail_exception")
        return False, msg
