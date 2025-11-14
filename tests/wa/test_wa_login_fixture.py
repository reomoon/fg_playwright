import pytest
from core.browser_manager import launch_browser, close_browser
from core.page_wrapper import create_highlighted_page
from pages.wa.wa_login import wa_login

# account 파라미터에 따라 로그인하는 fixture
@pytest.fixture(scope="function")
def wa_login_fixture(request):
    print("☑ wa_login fixture 실행됨")
    # pytest.mark.parametrize()에서 넘겨준 account 값을 가져옴
    account = request.param if hasattr(request, 'param') else "wa1"  # 기본값은 "wa2"

    # Playwright 컨텍스트와 브라우저를 초기화
    playwright, browser = launch_browser()

    # 래핑된 페이지 사용
    page = create_highlighted_page(browser)  

    # 불필요한 리소스 차단
    def block_resource(route):
        if route.request.resource_type in ["image"]:
            route.abort()
        else:
            route.continue_()

    page.route("**/*", block_resource)

    # beta 어드민 페이지 이동
    page.goto('https://beta-webadmin.fashiongo.net/', timeout=90000, wait_until="domcontentloaded") # 타임아웃 및 로드 이벤트 설정
    # 페이지 뷰포트를 최대화 크기로 설정
    page.set_viewport_size({"width": 1680, "height": 900})

    # 로그인 함수 호출(account 인수 그대로 호출)
    wa_login(page, account=account)

    # 페이지 로딩 3초 대기
    page.wait_for_timeout(3000)
  
    # assert 검증
    assert "webadmin.fashiongo" in page.url.lower()
    print("🅿 Beta WA URL 접속 성공")

    yield page #로그인된 페이지를 반환    
    close_browser(playwright, browser) # Playwright 컨텍스트와 브라우저 닫기