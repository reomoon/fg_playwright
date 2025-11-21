import pytest
from pages.front.orders.fr_order_openpack import order_openpack
from pages.front.orders.fr_order_prepack import order_prepack
from tests.front.login.test_front_login_fixture import front_login_fixture

@pytest.mark.parametrize("front_login_fixture", ["fr"], indirect=True)
def test_order_openpack(front_login_fixture):
    page = front_login_fixture    # 로그인된 페이지 사용
    # root에서 product_id 읽기
    with open("openpack_productid.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]
        product_id = lines[-1] if lines else ""
    print(f"☑ item productId: {product_id}")
    order_openpack(page, product_id)

@pytest.mark.parametrize("front_login_fixture", ["fr"], indirect=True)
def test_order_prepack(front_login_fixture):
    page = front_login_fixture    # 로그인된 페이지 사용
    # root에서 product_id 읽기
    with open("prepack_productid.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]
        product_id = lines[-1] if lines else ""
    print(f"☑ item productId: {product_id}")
    order_prepack(page, product_id)

   
