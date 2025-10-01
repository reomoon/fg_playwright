import pytest
from core.browser_manager import launch_browser, close_browser
from pages.va.va_login import va_login
from core.page_wrapper import create_highlighted_page

# @pytest.mark.asyncio: pytest.ini asyncio_mode = auto 설정해서 주석처리
def test_va_login():
    """
    VA 로그인 수동 테스트 실행
    """
    # Playwright 컨텍스트와 브라우저를 초기화
    playwright, browser = launch_browser()

    # 새 페이지 생성 후 하이라이트 래퍼로 감싸기
    page = create_highlighted_page(browser) 

    # va페이지 이동
    page.goto("https://beta-vendoradmin.fashiongo.net", timeout=90000, wait_until="domcontentloaded")

    # 페이지 뷰포트를 최대화 크기로 설정
    page.set_viewport_size({"width": 1680, "height": 900})

    # 로그인 함수 호출
    va_login(page)

    # 로그인 후 URL 검증
    # assert 검증
    assert "vendoradmin.fashiongo" in page.url.lower()
    print("🅿 Beta VA URL 접속 성공")

    # Playwright 컨텍스트와 브라우저 닫기
    close_browser(playwright, browser) 