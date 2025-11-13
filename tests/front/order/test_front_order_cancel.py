import pytest
from playwright.sync_api import Page
from pages.front.orders.fr_order_cancel import go_to_order_history
from pages.front.orders.fr_order_cancel import open_newly_placed_order_detail
from pages.front.orders.fr_order_cancel import cancel_order
from tests.front.login.test_front_login_fixture import front_login_fixture

def test_auto_cancel_newly_placed_order(front_login_fixture: Page):
    page = front_login_fixture

    go_to_order_history(page)
    open_newly_placed_order_detail(page)
    cancel_order(page)