import pytest
from core.browser_manager import launch_browser, close_browser
from core.page_wrapper import create_highlighted_page
from core.browser_devices import custom_devices
from pages.mobile.login.mo_login import mo_login

def mo_login(request):

    account = request.param if hasattr(request, 'param') else "mo"
    # Playwright 컨텍스트와 브라우저를 초기화
    playwright, browser = launch_browser()

    # 모바일 디바이스 에뮬레이션 추가
    context = browser.new_context(**custom_devices["iPhone 16"])  # iPhone 16 환경 적용

    page = create_highlighted_page(context)

    # 3. 테스트할 사이트로 이동
    page.goto("https://beta-www.fashiongo.net", timeout=90000, wait_until='domcontentloaded')

    # 4. 로그인 함수 실행
    mo_login(page, account=account)

    # 5. 브라우저 및 Playwright 엔진 종료
    yield page #로그인된 페이지를 반환  
    close_browser(playwright, browser)