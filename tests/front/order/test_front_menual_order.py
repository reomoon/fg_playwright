import pytest
from Pages.web.FR_Pages.orders.order_openpack_page import order_openpack
from Pages.web.FR_Pages.orders.order_prepack_page import order_prepack
from Pages.web.VA_Pages.va_create_items import va_create_items_openpack, va_create_items_prepack
from tests.web.FR_tests.test_login import login_fixture
from test_login import login_fixture

@pytest.mark.parametrize("login_fixture", ["fr"], indirect=True)
def test_order_openpack(login_fixture):
    page = login_fixture    # 로그인된 페이지 사용
    # root에서 product_id 읽기
    with open("created_openpack_id.txt", "r") as f:
        product_id = f.read().strip()
    order_openpack(page, product_id)

@pytest.mark.parametrize("login_fixture", ["fr"], indirect=True)
def test_order_prepack(login_fixture):
    page = login_fixture    # 로그인된 페이지 사용
    # root에서 product_id 읽기
    with open("created_prepack_id.txt", "r") as f:
        product_id = f.read().strip()
    order_prepack(page, product_id)

   
