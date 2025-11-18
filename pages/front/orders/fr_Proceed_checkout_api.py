import re
from playwright.sync_api import Page

def proceed_to_checkout(page: Page):
    # 1. 장바구니 페이지로 이동
    page.goto("https://beta-www.fashiongo.net/Cart")
    page.wait_for_selector("button.btn-checkoutAll", timeout=10000)

    # 👉 2. 특정 벤더의 "Check Out This Vendor Only" 버튼 클릭
    #    - 현재 예시: div id="order16502" 안에 있는 btn-checkoutVendor
    vendor_order_id = "16502"
    vendor_checkout_sel = f'div#order{vendor_order_id} button.btn-checkoutVendor'

    # 버튼이 뜰 때까지 대기
    page.wait_for_selector(vendor_checkout_sel, timeout=10000)
    print("☑ Check Out This Vendor Only 버튼 찾음")

    # 버튼 클릭
    page.locator(vendor_checkout_sel).click()
    print("🅿 특정 벤더 체크아웃 버튼 클릭 완료")

    # 2-1. 프로모션 모달 확인 및 처리
    try:
        # 모달이 표시될 가능성이 있으므로 잠시 대기
        modal_visible = page.wait_for_selector(
            "div.modal_beforeCheckout",
            state="visible",
            timeout=3000
        )
        if modal_visible:
            print("☑ 프로모션 모달 감지됨")
            # "Continue To Checkout" 버튼 클릭
            page.locator("div.modal_beforeCheckout button.btn-sure").click()
            print("🅿 Continue To Checkout 버튼 클릭 완료")
    except:
        print("☑ 프로모션 모달 없음 → 바로 진행")

    # 3. 이동한 URL에서 sessionId 추출
    page.wait_for_url(re.compile(r"^https://beta-www\.fashiongo\.net/Checkout/.*"))
    checkout_url = page.url
    print(f"[URL] 이동 완료: {checkout_url}")

    match = re.search(r'/Checkout/([^/?]+)', checkout_url)
    session_id = match.group(1) if match else None

    if session_id:
        print(f"[✅ sessionId 추출 성공] {session_id}")
        return session_id
    else:
        print("[❌ sessionId 추출 실패]")
        return None