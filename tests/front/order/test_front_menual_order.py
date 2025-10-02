import pytest
from pages.front.orders.fr_order_openpack import order_openpack
from pages.front.orders.fr_order_prepack import order_prepack
from tests.front.login.test_front_login_fixture import front_login_fixture

@pytest.mark.parametrize("front_login_fixture", ["fr"], indirect=True)
def test_order_openpack(front_login_fixture):
    page = front_login_fixture    # 로그인된 페이지 사용
    # root에서 product_id 읽기
    with open("created_openpack_id.txt", "r") as f:
        product_id = f.read().strip()
    order_openpack(page, product_id)

@pytest.mark.parametrize("front_login_fixture", ["fr"], indirect=True)
def test_order_prepack(front_login_fixture):
    page = front_login_fixture    # 로그인된 페이지 사용
    # root에서 product_id 읽기
    with open("created_prepack_id.txt", "r") as f:
        product_id = f.read().strip()
    order_prepack(page, product_id)

   
