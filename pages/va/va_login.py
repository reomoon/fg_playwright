from core.page_wrapper import create_highlighted_page
import re

# Pages/front login
def va_login(page, account="va"):
    from core.page_account import LOGIN_CREDENTIALS # 함수 내부에서 임포트

    # 로그인 정보 가져오기 (전역 변수 LOGIN_CREDENTIALS 사용)
    username_key = f"{account}_username"
    password_key = f"{account}_password"

    try:
        username = LOGIN_CREDENTIALS[username_key]
        password = LOGIN_CREDENTIALS[password_key]
    except KeyError as e:
        raise ValueError(f"LOGIN_CREDENTIALS {e} 키가 없습니다.")

    # 로그인 요소 정의 및 동작
    username_input = page.locator('input[formcontrolname="userName"]')
    page.wait_for_timeout(1000) # 1초 대기
    username_input.fill(username)
    password_input = page.locator('input[formcontrolname="password"]')
    password_input.fill(password)

    # SECURE LOGIN
    page.locator('.btn.btn-blue.width-100p.btn-login').click()
    print(f"☑ VA_{account} 계정 로그인 완료")

    # 페이지 로딩 상태를 기다림
    # page.wait_for_url("**/home", timeout=30000)
    page.wait_for_url(re.compile(r"https://beta-vendoradmin\.fashiongo\.net/#/home(?:\?.*)?$"), timeout=60000)
    print("🅿 VA URL ok:", page.url)

    # Net Terms 팝업 닫기
    netterms_popup_element = page.locator('div.label', has_text = "Don't show again today")

    if netterms_popup_element.is_visible(): # netterms_popup_element 실제 화면에 렌더링되어 보이는지 여부까지 체크 → 보일 때만 클릭 실행 → 클릭 에러 방지
        try:
            netterms_popup_element.click()  # 오늘 하루 보지 않기 체크박스 클릭
            page.locator('i.modal-close-btn').nth(1).click()  # Net Terms팝업 닫기
            print("☑ Net Terms 팝업 24시간 안보이기를 클릭 했습니다.")
        except Exception as e:
            print(f"Net Terms 팝업 클릭 중 에러 발생:{e}")
    else:
        print("☑ Net Terms 팝업이 없습니다.")
    
