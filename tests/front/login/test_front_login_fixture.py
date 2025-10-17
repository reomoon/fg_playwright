import pytest
from core.browser_manager import launch_browser, close_browser
from core.page_wrapper import create_highlighted_page
from pages.front.login.fr_login import front_login

# account 파라미터에 따라 로그인하는 fixture
"""
pytest의 fixture에서 scope="module"과 scope="function"의 차이는 다음과 같습니다:

scope="function":
각 테스트 함수마다 fixture가 매번 새로 실행됩니다.
(테스트 함수마다 독립적인 환경이 필요할 때 사용)

scope="module":
하나의 테스트 파일(모듈) 내에서 fixture가 한 번만 실행되고,
그 결과가 파일 내 모든 테스트 함수에서 공유됩니다.
(비용이 큰 초기화 작업을 여러 테스트가 공유할 때 사용)
"""

@pytest.fixture(scope="function")
def front_login_fixture(request):
    print("☑ fr_login fixture 실행됨")
    # pytest.mark.parametrize()에서 넘겨준 account 값을 가져옴
    account = request.param if hasattr(request, 'param') else "fr"  # 기본값은 "fr"

    # Playwright 컨텍스트와 브라우저를 초기화
    playwright, browser = launch_browser()

    # HighlightPageWrapper를 사용하여 새 페이지 생성 및 래핑
    page = create_highlighted_page(browser)
    page.goto("https://www.fashiongo.net", timeout=90000, wait_until='domcontentloaded')  # 페이지 로딩 대기
    
    # 페이지 뷰포트 크기 설정
    page.set_viewport_size({"width": 1680, "height": 900})

    # 로그인 함수 호출
    front_login(page, account=account)
    
    yield page #로그인된 페이지를 반환    
    close_browser(playwright, browser) # Playwright 컨텍스트와 브라우저 닫기