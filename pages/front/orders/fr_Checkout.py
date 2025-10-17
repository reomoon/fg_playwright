from playwright.sync_api import Page
from pathlib import Path

def capture_screenshot(page: Page, name: str):
    path = Path(f"screenshots/{name}.png")
    path.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=path)
    print(f"[스크린샷 저장] {path}")

def click_button_safe(page: Page, selector: str, name: str, timeout=5000):
    try:
        page.wait_for_selector(selector, timeout=timeout)
        button = page.locator(selector)
        button.click()
        print(f"[클릭 성공] {name}")
        return True
    except Exception as e:
        print(f"[클릭 실패] {name} - {e}")
        capture_screenshot(page, f"fail_{name.replace(' ', '_')}")
        return False

def Checkout_flow(page: Page):
    # 1. 쇼핑백 페이지 진입
    page.goto("https://www.fashiongo.net/cart")

    # 1-1. Checkout 버튼 클릭
    if not click_button_safe(page, 'button.btn-checkoutAll', "Checkout Vendor"):
        return False

    # 1-2. 모달 확인
    modal_detected = False
    try:
        for _ in range(30):
            modal_visible = page.evaluate("""() => {
                const modal = document.querySelector('div.modal_beforeCheckout');
                return modal && window.getComputedStyle(modal).display === 'block';
            }""")
            if modal_visible:
                print("[모달 감지됨] display: block")
                modal_detected = True
                break
            page.wait_for_timeout(100)
    except Exception as e:
        print(f"[모달 체크 중 예외 발생] {e}")
        capture_screenshot(page, "fail_modal_check_exception")

    if modal_detected:
        try:
            modal_button = page.locator('div.modal_beforeCheckout button.btn-sure')
            if modal_button.is_visible():
                modal_button.click()
                print("[클릭 성공] 모달 내 Continue To Checkout")
            else:
                print("[클릭 실패] 모달 내 버튼이 visible하지 않음")
                capture_screenshot(page, "fail_Continue_To_Checkout_not_visible")
                return False
        except Exception as e:
            print(f"[모달 처리 중 예외 발생] {e}")
            capture_screenshot(page, "fail_modal_exception")
            return False
    else:
        print("[모달 없음] 모달 무시하고 진행")

    # 2. 체크아웃 1단계 → 2단계
    page.wait_for_load_state("load")
    page.wait_for_selector("button.btn-goToPayment", timeout=15000)
    if not click_button_safe(page, 'button.btn-goToPayment', "Save & Continue - Step1"):
        return False

    # 3. 체크아웃 2단계 → 3단계
    page.wait_for_load_state("load")
    if not click_button_safe(page, 'button.btn-goToReview', "Save & Continue - Step2"):
        return False

    # 4. 체크아웃 3단계 → Submit Order
    page.wait_for_load_state("load")
    if not click_button_safe(page, 'button.btn-checkout', "Submit Order"):
        return False

    # 5. 오더 번호 추출
    page.wait_for_load_state("load")
    try:
        page.wait_for_selector("a.link-order", timeout=10000)
        order_no = page.locator("a.link-order").inner_text().strip()
        print(f"[오더번호 추출 완료] {order_no}")
    except:
        print("[오더번호 추출 실패] - 스크린샷 캡처")
        capture_screenshot(page, "fail_order_no")
        return False

    # 6. 오더 히스토리에서 오더번호 확인
    page.goto("https://www.fashiongo.net/MyAccount/OrderHistory")
    try:
        for _ in range(50):
            order_sn_locator = page.locator("span.order-sn").filter(has_text=order_no)
            if order_sn_locator.first.is_visible():
                print(f"[오더 확인 완료] 오더번호 {order_no} 이력에 존재함")
                break
            page.wait_for_timeout(200)
        else:
            print(f"[오더 확인 실패] 오더번호 {order_no} 이력에 없음")
            capture_screenshot(page, "fail_order_history")
            return False
    except Exception as e:
        print(f"[오더 히스토리 페이지 오류] {e}")
        capture_screenshot(page, "fail_order_history_page")
        return False

    # 7. 오더 디테일 페이지 진입 및 오더번호 확인
    try:
        # 오더 이력 리스트에서 오더 넘버 클릭
        order_sn_locator.first.click()
        page.wait_for_load_state("networkidle")  # 안정적으로 페이지 로딩 대기

        # 디테일 페이지에서 h1 텍스트 가져오기
        page.wait_for_selector("div.tit_bx h1", timeout=10000)
        h1_text = page.locator("div.tit_bx h1").inner_text().strip()

        if order_no in h1_text:
            print(f"[디테일 페이지 확인 완료] 오더번호 {order_no} 표시됨")
            return True
        else:
            print(f"[디테일 페이지 확인 실패] h1 텍스트에 오더번호 {order_no} 없음")
            capture_screenshot(page, "fail_order_detail_h1_mismatch")
            return False

    except Exception as e:
        print(f"[디테일 페이지 확인 중 예외 발생] {e}")
        capture_screenshot(page, "fail_order_detail_page_exception")
        return False
