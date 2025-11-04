import pytest
from pages.front.items.fr_AddtoCart_api import add_item_to_cart
from pages.front.orders.fr_Proceed_checkout_api import proceed_to_checkout
from pages.front.orders.fr_PlaceOrder_api import place_order
from tests.front.login.test_front_login_fixture import front_login_fixture

def test_place_order_flow(front_login_fixture):
    page = front_login_fixture

    # 1. 장바구니에 상품 추가
    add_item_to_cart(page)

    # 2. Checkout 진입 및 sessionId 추출
    session_id = proceed_to_checkout(page)
    assert session_id is not None, "❌ sessionId 추출 실패"

    # 3. 주문 제출
    success = place_order(page, session_id)
    assert success is True, "❌ 주문 제출 실패"