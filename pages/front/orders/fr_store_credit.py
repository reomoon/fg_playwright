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

def Checkout_store_credit_flow(page: Page):
    # 1. 쇼핑백 페이지 진입
    page.goto("https://beta-www.fashiongo.net/cart")

    # 1-1. Checkout 버튼 클릭
    # if not click_button_safe(page, 'button.btn-checkoutAll', "Checkout Vendor"):
    #    return False
    
    # 1-1. Checkout this vendor only 버튼 클릭
    order_id = "16502"  # 이미 있다면 이 줄은 생략
    selector = f'#order{order_id} button.btn-checkoutVendor'

    if not click_button_safe(page, selector, "Checkout Vendor Only"):
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

    # 🔹 2-1. Payment(체크아웃 2단계)에서 Store Credit 문구 노출 확인
    try:
        print("☑ Payment 단계 Store Credit 문구 확인 시작")
        # Payment 요약 영역 로딩 대기
        page.wait_for_selector("div.points-price dl.jsCreditInfo dt", timeout=10000)

        dt_locator = page.locator("div.points-price dl.jsCreditInfo dt")
        dt_text = dt_locator.inner_text().strip()

        if "Store Credit" in dt_text:
            print(f"🅿 Store Credit 문구 노출 확인 (dt 텍스트: {dt_text})")
        else:
            print(f"❌ dt 텍스트에 'Store Credit' 문구가 포함되지 않음 (현재: {dt_text})")
            capture_screenshot(page, "fail_store_credit_text")
            return False
    except Exception as e:
        print(f"❌ Store Credit 문구 확인 중 예외 발생: {e}")
        capture_screenshot(page, "fail_store_credit_exception")
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
    page.goto("https://beta-www.fashiongo.net/MyAccount/OrderHistory")
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

    # 7. 오더 디테일 페이지 진입 및 오더번호 확인 + Store Credit 금액 검증
    try:
        # 오더 이력 리스트에서 오더 넘버 클릭
        order_sn_locator.first.click()
        page.wait_for_load_state("networkidle")  # 안정적으로 페이지 로딩 대기

        # 디테일 페이지에서 h1 텍스트 가져오기 (Order No 확인)
        page.wait_for_selector("div.tit_bx h1", timeout=10000)
        h1_text = page.locator("div.tit_bx h1").inner_text().strip()

        if order_no in h1_text:
            print(f"[디테일 페이지 확인 완료] 오더번호 {order_no} 표시됨")
        else:
            print(f"[디테일 페이지 확인 실패] h1 텍스트에 오더번호 {order_no} 없음")
            capture_screenshot(page, "fail_order_detail_h1_mismatch")
            return False

        # 🔹 Store Credit 금액 -$200.00 표시 여부 확인
        try:
            print("☑ 디테일 페이지 Store Credit 금액 확인 시작")
            # price_info 블럭 로딩 대기
            page.wait_for_selector("div.price_info", timeout=10000)

            # li 중에서 'Store Credit:' 이 포함된 행 찾기
            store_credit_li = page.locator("div.price_info li").filter(has_text="Store Credit:")
            if not store_credit_li.first.is_visible():
                print("❌ Store Credit 행(li)이 보이지 않습니다.")
                capture_screenshot(page, "fail_detail_store_credit_li_not_visible")
                return False

            # 해당 li 안의 span.price.discount 값 읽기
            store_credit_value = store_credit_li.first.locator("span.price.discount").inner_text().strip()
            print(f"☑ 디테일 페이지 Store Credit 표시 값: {store_credit_value}")

            expected_value = "-$200.00"
            if store_credit_value == expected_value:
                print(f"🅿 Store Credit 금액 {expected_value} 표시 확인 완료")
                return True
            else:
                print(f"❌ Store Credit 금액 불일치 (기대값: {expected_value}, 실제값: {store_credit_value})")
                capture_screenshot(page, "fail_detail_store_credit_value_mismatch")
                return False

        except Exception as e:
            print(f"❌ 디테일 페이지 Store Credit 금액 확인 중 예외 발생: {e}")
            capture_screenshot(page, "fail_detail_store_credit_exception")
            return False

    except Exception as e:
        print(f"[디테일 페이지 확인 중 예외 발생] {e}")
        capture_screenshot(page, "fail_order_detail_page_exception")
        return False