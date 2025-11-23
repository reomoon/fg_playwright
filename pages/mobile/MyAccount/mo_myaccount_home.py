from core.page_wrapper import create_highlighted_page
from core.close_by_close_buttons import close_by_close_mobile

def mobile_myaccount(page):
    # App 배너 닫기
    app_popup = page.locator('a.close-get-app-bnr', has_text="close")
    if app_popup.is_visible():
        app_popup.click()
           
    # 모든 팝업 닫기
    close_by_close_mobile(page)
    page.wait_for_timeout(1000)  # 1초 대기

    # My Account 이동
    page.goto("https://beta-mobile.fashiongo.net/account")

    # /account 페이지 출력되면 성공
    page.wait_for_url("**/account", timeout=5000)
    if "/account" in page.url: # /account가 페이지 url안에 있으면
        print("☑ /account 페이지 진입 성공")
    else: # url이 없다면
        print("❌ /account 페이지 진입 실패")
        return False
