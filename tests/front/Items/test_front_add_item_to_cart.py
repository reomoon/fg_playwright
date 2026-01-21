from playwright.sync_api import Page, expect
from pages.front.items.fr_AddtoCart import run_add_to_cart_flow
from tests.front.login.test_front_login_fixture import front_login_fixture

def test_add_item_to_cart(front_login_fixture):
    run_add_to_cart_flow(front_login_fixture)

    