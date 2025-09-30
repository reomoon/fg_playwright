import pytest
from pages.wa.wa_login import wa_login
from core.browser_manager import launch_browser, close_browser
from core.page_wrapper import create_highlighted_page

async def test_wa_login():
    """
    WA login 수동 테스트 실행
    """
    # playwright context 브라우저 초기화
    playwright, browser = await launch_browser()

    # 새 페이지 생성 후 하이라이트 래퍼로 감싸기
    page = await create_highlighted_page(browser) 

    # 페이지 이동
    await page.goto("https://beta-webadmin.fashiongo.net", timeout=90000, wait_until="domcontentloaded")

    # wa_log 함수 실행
    await wa_login(page, account="wa2")

    # assert 검증
    assert "webadmin.fashiongo" in page.url.lower()
    print("🅿 Beta WA URL 접속 성공")

    # 브라우저 닫기
    await close_browser(playwright, browser)





