import pytest
from core.browser_manager import launch_browser, close_browser
from pages.va.va_login import va_login
from core.page_wrapper import create_highlighted_page

@pytest.fixture(scope="function")
async def va_login_fixture(request):
    # Playwright 컨텍스트와 브라우저를 초기화
    playwright, browser = await launch_browser()

    # 새 페이지 생성 후 하이라이트 래퍼로 감싸기
    page = await create_highlighted_page(browser) 

    # va페이지 이동
    await page.goto("https://beta-vendoradmin.fashiongo.net", timeout=90000, wait_until="domcontentloaded")

    # 페이지 뷰포트를 최대화 크기로 설정
    page.set_viewport_size({"width": 1680, "height": 900})

    # 로그인 함수 호출
    va_login(page)

    # 로그인 후 URL 검증
    # assert 검증
    assert "vendoradmin.fashiongo" in page.url.lower()
    print("🅿 Beta VA URL 접속 성공")

    yield page #로그인된 페이지를 반환    
    await close_browser(playwright, browser) # Playwright 컨텍스트와 브라우저 닫기