from core.page_wrapper import HighlightPageWrapper

def front_login(page, account="fr"):
    from core.page_account import LOGIN_CREDENTIALS

    # 키 이름 생성
    username_key = f"{account}_username"
    password_key = f"{account}_password"

    # 로그인 정보 가져오기
    try:
        username = LOGIN_CREDENTIALS[username_key]
        password = LOGIN_CREDENTIALS[password_key]
    except KeyError as e:
        raise ValueError(f"LOGIN_CREDENTIALS {e} 키가 없습니다.")

    # 해당 계정의 사용자 이름과 비밀번호가 없을 경우 예외처리
    if not username or not password:
        raise ValueError(f"Missing credentials for account type: {account}")
    
    # 쿠키 동의 버튼
    try:
        cookie_button = page.locator('#onetrust-accept-btn-handler')
        if cookie_button.is_visible():
            cookie_button.click()
    except:
        pass

    # 헤더 로그인 버튼 클릭
    page.locator('a.header_signIn').click()
    page.wait_for_timeout(3000) # 3초 대기
    
    # username / password 입력
    # fill은 채우기만 해서 .signin_btn 이벤트가 트리거가 안되서 로그인 버튼이 비활성화로 남아있음
    username_input = page.locator('input[name="userName"]') 
    username_input.type(username, delay=50)
    password_input = page.locator('input[name="password"]')
    password_input.type(password, delay=50)

    # 로그인 버튼 클릭
    with page.expect_navigation(wait_until="domcontentloaded", timeout=60000):
        page.locator('.signin_btn').click()

    # 대기
    page.wait_for_timeout(1000)

    assert "www.fashiongo" in page.url.lower()
    print("🅿 Beta Front URL 접속 성공")

    # Needs Attention 팝업 24시간 안보이기( # 'for="personal-2"' 속성으로 label을 클릭)
    # try:
    #     page.locator('label[for="personal-2"]').last.click()
    # except:
    #     pass  # 팝업이 없으면 무시하고 계속 진행

    # Free Shipping 팝업 24시간 안보이기
    # page.locator_popup('a.link-footer-sub.btn-hide-popup').click()

