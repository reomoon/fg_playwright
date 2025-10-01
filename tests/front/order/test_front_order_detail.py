import pytest
from playwright.sync_api import sync_playwright, Page
from test_login import login_fixture
from Pages.web.FR_Pages.orders.Checkout import Checkout_flow

def test_OrderDetail(login_fixture: Page):
    # 로그인 후 페이지 객체를 받아와서 체크아웃 흐름 테스트
    result = Checkout_flow(login_fixture)
    assert result is True, "체크아웃 흐름 실패"