import pytest
from pages.wa.wa_login import wa_login
from core.browser_manager import launch_browser, close_browser
from core.page_wrapper import create_highlighted_page

def test_wa_login():
    """
    WA login 수동 테스트 실행
    """
    # playwright context 브라우저 초기화
    playwright, browser = launch_browser()

    # 새 페이지 생성 후 하이라이트 래퍼로 감싸기
    page = create_highlighted_page(browser) 

    # 페이지 이동
    page.goto("https://webadmin.fashiongo.net", timeout=90000, wait_until="domcontentloaded")

    # wa_log 함수 실행
    wa_login(page, account="wa2")

    # assert 검증
    assert "webadmin.fashiongo" in page.url.lower()
    print("🅿 Beta WA URL 접속 성공")

    # 브라우저 닫기
    close_browser(playwright, browser)





