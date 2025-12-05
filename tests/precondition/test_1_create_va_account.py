import pytest
from core.browser_manager import launch_browser, close_browser
from core.page_wrapper import create_highlighted_page
from pages.wa.wa_login_token import wa_login_token
from pages.wa.wa_create_va_account import create_vendor_account

@pytest.fixture
def page():
    """WA 로그인용 page fixture"""
    playwright, browser = launch_browser()
    page = create_highlighted_page(browser)
    
    yield page
    
    close_browser(playwright, browser)

def test_create_vendor_account(page):
    """벤더 계정 생성 테스트"""
    # 1. wa_login_token으로 로그인 및 토큰 획득
    page = wa_login_token(page, account="wa2")
    
    # 2. 벤더 계정 생성
    create_vendor_account(page)