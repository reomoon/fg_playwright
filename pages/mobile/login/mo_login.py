from core.page_wrapper import HighlightPageWrapper
from core.close_by_close_buttons import close_by_close_mobile

# Pages/mobile_login
def mo_login(page, account="mo"):
    from core.page_account import LOGIN_CREDENTIALS # 함수 내부에서 임포트

    # 로그인 정보 가져오기 (전역 변수 LOGIN_CREDENTIALS 사용)
    mo_username = LOGIN_CREDENTIALS[f"{account}_username"]
    mo_password = LOGIN_CREDENTIALS[f"{account}_password"]

    # Accept All Cookies 선택
    page.locator('#onetrust-accept-btn-handler').click()

    page.wait_for_timeout(3000)  # 3초(3000ms) 대기

    # App 배너 닫기
    app_popup = page.locator('a.close-get-app-bnr', has_text="close")
    if app_popup.is_visible():
        app_popup.click()
           
    # 모든 팝업 닫기
    close_by_close_mobile(page)

    # Footer Account 선택
    try:
        page.wait_for_selector('ion-label', has_text="Account", timeout=5000)
        account_label = page.locator('ion-label', has_text="Account", log_if_not_found=False)
        if account_label.is_visible():
            account_label.click()
            print("☑ Footer Account를 클릭 하였습니다.")
        else:
            print("🗙 Footer Account label이 보이지 않습니다. 로그인 페이지로 이동합니다.")
            page.goto('https://beta-mobile.fashiongo.net/login')
            page.wait_for_timeout(1000)
    except Exception:
        print("🗙 Footer Account label 대기 실패. 로그인 페이지로 이동합니다.")
        page.goto('https://beta-mobile.fashiongo.net/login')
        page.wait_for_timeout(1000)
    
    # 로그인 요소 정의 및 동작
    # page.locator('button.btn-sign-in.nclick', log_if_not_found=False).click()

    # 3초 대기
    page.wait_for_timeout(3000)

    username_input = page.locator('input[formcontrolname="userName"]') # fill은 채우기만 해서 이벤트가 트리거 안됨
    username_input.type(mo_username, delay=50)
    password_input = page.locator('input[formcontrolname="password"]')
    password_input.type(mo_password, delay=50)
    
    # Sign In 버튼(button.nclick 같은 요소가 밑에도 있어 first 추가하여 첫 번째 버튼 클릭)
    page.locator('button.button.nclick').first.click()

    # 페이지 로딩 상태를 기다림(로그인 후 로딩 딜레이 있어 조건 추가)
    page.wait_for_timeout(3000) # 1초 대기