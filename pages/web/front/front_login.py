from core.page_wrapper import HighlightPageWrapper
from core.browser_manager import launch_browser, close_browser

async def front_login(page, account="fr"):
    from core.page_account import LOGIN_CREDENTIALS

    # 키 이름 생성
    username_key = f"{account}_username"
    password_key = f"{account}_password"

    # 로그인 정보 가져오기
    username = LOGIN_CREDENTIALS[username_key]
    password = LOGIN_CREDENTIALS[password_key]

    # 해당 계정의 사용자 이름과 비밀번호가 없을 경우 예외처리
    if not username or not password:
        raise ValueError(f"Missing credentials for account type: {account}")
    
    # 쿠키 동의 버튼
    try:
        cookie_button = page.locator('#onetrust-accept-btn-handler')
        if await cookie_button.is_visible():
            await cookie_button.click()
    except:
        pass

    # 로그인 버튼 클릭
    await page.locator('a.header_signIn').click()
    await page.wait_for_timeout(3000) # 3초 대기
    
    username_input = page.locator('input[name="userName"]') # fill은 채우기만 해서 이벤트가 트리거가 안됨
    await username_input.type(username)
    password_input = page.locator('input[name="password"]')
    await password_input.type(password)
    
    async with page.expect_navigation(): # async with로 변경
        await page.locator('.signin_btn').click()
    
    # 3초 대기
    await page.wait_for_timeout(3000)

    # Needs Attention 팝업 24시간 안보이기( # 'for="personal-2"' 속성으로 label을 클릭)
    # try:
    #     await page.locator('label[for="personal-2"]').last.click()
    # except:
    #     pass  # 팝업이 없으면 무시하고 계속 진행

    # Free Shipping 팝업 24시간 안보이기
    # await page.locator_popup('a.link-footer-sub.btn-hide-popup').click()

