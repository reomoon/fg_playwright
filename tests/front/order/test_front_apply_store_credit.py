from playwright.sync_api import Page
from tests.front.login.test_front_login_fixture import front_login_fixture
from pages.front.orders.fr_store_credit import Checkout_store_credit_flow
from pages.front.items.fr_AddtoCart_api import add_item_to_cart


def test_place_order(front_login_fixture: Page):
    page = front_login_fixture

    print("🅰 Front 계정 로그인 완료 - 장바구니 담기 시작")
    add_item_to_cart(page)
    print("🅿 장바구니 담기 완료 - 스토어 크레딧 체크아웃 플로우 시작")

    success, message = Checkout_store_credit_flow(page)
    assert success, message