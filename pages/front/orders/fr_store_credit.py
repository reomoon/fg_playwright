from playwright.sync_api import Page
from pathlib import Path


def capture_screenshot(page: Page, name: str):
    path = Path(f"screenshots/{name}.png")
    path.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=path)
    print(f"🗙 [스크린샷 저장] {path}")


def click_button_safe(page: Page, selector: str, step_name: str, timeout: int = 5000) -> bool:
    print(f"☑ [{step_name}] 버튼 찾기 시도: {selector}")
    try:
        page.wait_for_selector(selector, state="visible", timeout=timeout)
        button = page.locator(selector).first
        button.scroll_into_view_if_needed()
        button.click(timeout=timeout)
        print(f"🅿 [{step_name}] 버튼 클릭 성공")
        return True
    except Exception as e:
        print(f"❌ [{step_name}] 버튼 클릭 실패 - {e}")
        capture_screenshot(page, f"fail_{step_name.replace(' ', '_')}")
        return False


def Checkout_store_credit_flow(page: Page):
    """
    반환값: (success: bool, message: str)
    STEP5 - Payment 단계 Store Credit 문구 확인 성공 시 PASS 처리
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
    order_id = "16502"
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
        if "Execution context was destroyed" in str(e):
            print(f"☑ {step}: 네비게이션 감지, 모달 없이 진행")
            modal_detected = False
        else:
            msg = f"{step} 실패: 모달 체크 중 예외 발생 ({e})"
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
        msg = f"{step} 실패: 버튼 노출 안 됨 ({e})"
        print(f"❌ {msg}")
        capture_screenshot(page, "fail_step4_button_not_found")
        return False, msg

    if not click_button_safe(page, "button.btn-goToPayment", step_name=step):
        msg = f"{step} 실패: 버튼 클릭 실패"
        return False, msg

    # ─────────────────────────────
    # STEP 5. Payment 단계 Store Credit 문구 확인 (PASS 기준)
    # ─────────────────────────────
    step = "STEP5 - Payment 단계 Store Credit 문구 확인"
    print(f"☑ {step}")
    try:
        page.wait_for_selector("div.points-price dl.jsCreditInfo dt", timeout=10000)
        dt_text = page.locator("div.points-price dl.jsCreditInfo dt").inner_text().strip()

        if "Store Credit" in dt_text:
            print(f"🅿 {step} 완료 - dt 텍스트: {dt_text}")
            print("🅿 STEP5 성공 → 테스트 PASS 처리")
            return True, "STEP5 - Store Credit 문구 확인 성공"
        else:
            msg = f"{step} 실패: 'Store Credit' 문구 미포함 (현재: {dt_text})"
            print(f"❌ {msg}")
            capture_screenshot(page, "fail_store_credit_text")
            return False, msg

    except Exception as e:
        msg = f"{step} 실패: Store Credit 문구 확인 중 예외 발생 ({e})"
        print(f"❌ {msg}")
        capture_screenshot(page, "fail_store_credit_exception")
        return False, msg