from playwright.sync_api import sync_playwright, Page
from tests.front.login.test_front_login_fixture import front_login_fixture
from pages.front.orders.fr_Checkout import Checkout_flow

def test_OrderDetail(front_login_fixture: Page):
    # 로그인 후 페이지 객체를 받아와서 체크아웃 흐름 테스트
    result = Checkout_flow(front_login_fixture)
    assert result is True, "체크아웃 흐름 실패"