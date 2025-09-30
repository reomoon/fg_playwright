from core.page_wrapper import create_highlighted_page

# Pages/mobile_login
async def login(page):
    from core.page_account import LOGIN_CREDENTIALS  # 함수 내부에서 임포트

    # 로그인 정보 가져오기 (전역 변수 LOGIN_CREDENTIALS 사용)
    mo_username = LOGIN_CREDENTIALS["mo_username"]
    mo_password = LOGIN_CREDENTIALS["mo_password"]

    # Accept All Cookies 선택
    await page.locator('#onetrust-accept-btn-handler').click()

    # Footer Account 선택
    await page.locator('ion-label', has_text="Account").click()

    await page.wait_for_timeout(1000)  # 1초 대기

    # App 배너 닫기
    await page.locator_popup('a.close-get-app-bnr', has_text="close").click()

    # 로그인 요소 정의 및 동작
    await page.locator('button.btn-sign-in.nclick').click()
    await page.wait_for_timeout(3000)

    username_input = page.locator('input[formcontrolname="userName"]')
    await username_input.fill(mo_username)
    password_input = page.locator('input[formcontrolname="password"]')
    await password_input.fill(mo_password)

    # Sign In 버튼 클릭 (첫 번째 버튼)
    await page.locator('button.button.nclick').first.click()

    # 페이지 로딩 상태를 기다림(로그인 후 로딩 딜레이)
    await page.wait_for_timeout(1000)

    # Needs Attention 팝업 24시간 안보이기
    await page.locator_popup('label[for="personal-2"]').last.click()

    # Free Shipping 팝업 닫기
    await page.locator_popup('span.icon_close').click()