import pytest
from core.browser_manager import launch_browser, close_browser
from core.page_wrapper import create_highlighted_page
from pages.front.login.fr_login import front_login

# account 파라미터에 따라 로그인하는 fixture
@pytest.fixture(scope="function")
def front_login_fixture(request):
    # pytest.mark.parametrize()에서 넘겨준 account 값을 가져옴
    account = request.param if hasattr(request, 'param') else "fr"  # 기본값은 "fr"

    # Playwright 컨텍스트와 브라우저를 초기화
    playwright, browser = launch_browser()

    # HighlightPageWrapper를 사용하여 새 페이지 생성 및 래핑
    page = create_highlighted_page(browser)
    page.goto("https://beta-www.fashiongo.net", timeout=90000, wait_until='domcontentloaded')  # 페이지 로딩 대기
    
    # 페이지 뷰포트 크기 설정
    page.set_viewport_size({"width": 1680, "height": 900})

    # 로그인 함수 호출
    front_login(page, account=account)
    
    yield page #로그인된 페이지를 반환    
    close_browser(playwright, browser) # Playwright 컨텍스트와 브라우저 닫기