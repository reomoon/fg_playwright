import re
from playwright.sync_api import Page

def proceed_to_checkout(page: Page):
    # 1. 장바구니 페이지로 이동
    page.goto("https://beta-www.fashiongo.net/Cart")
    page.wait_for_selector("button.btn-checkoutAll", timeout=10000)

    # 2. Checkout 버튼 클릭
    page.locator("button.btn-checkoutAll").click()

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