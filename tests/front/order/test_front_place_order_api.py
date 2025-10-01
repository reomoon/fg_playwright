import pytest
from Pages.web.FR_Pages.Items.Addtocart_api import add_item_to_cart
from Pages.web.FR_Pages.orders.Proceed_checkout_api import proceed_to_checkout
from Pages.web.FR_Pages.orders.Placeorder_api import place_order
from test_login import login_fixture

@pytest.mark.parametrize("login_fixture", ["fr"], indirect=True)
def test_place_order_flow(login_fixture):
    page = login_fixture

    # 1. 장바구니에 상품 추가
    add_item_to_cart(page)

    # 2. Checkout 진입 및 sessionId 추출
    session_id = proceed_to_checkout(page)
    assert session_id is not None, "❌ sessionId 추출 실패"

    # 3. 주문 제출
    success = place_order(page, session_id)
    assert success is True, "❌ 주문 제출 실패"