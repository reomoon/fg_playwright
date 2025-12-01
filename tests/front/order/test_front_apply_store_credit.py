from playwright.sync_api import sync_playwright, Page
from tests.front.login.test_front_login_fixture import front_login_fixture
from pages.front.orders.fr_store_credit import Checkout_store_credit_flow
from pages.front.items.fr_AddtoCart_api import add_item_to_cart

def test_place_order(front_login_fixture):
    page = front_login_fixture
    add_item_to_cart(page)
    # 로그인 후 페이지 객체를 받아와서 체크아웃 흐름 테스트
    result = Checkout_store_credit_flow(front_login_fixture)
    assert result is True, "체크아웃 흐름 실패"