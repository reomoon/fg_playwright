import pytest
from pages.mobile.order.mo_order_openpack import mobile_order_openpack
from pages.mobile.order.mo_order_prepack import mobile_order_prepack
from tests.mobile.login.test_mobile_login_fixture import mo_login_fixture

@pytest.mark.parametrize("mo_login_fixture", ["mo"], indirect=True)
def test_order_openpack(mo_login_fixture):
    page = mo_login_fixture    # 로그인된 페이지 사용
    # root에서 product_id 읽기
    with open("output\\created_openpack_id.txt", "r") as f:
        product_id = f.read().strip()
    mobile_order_openpack(page, product_id)    # order_openpack 실행
    # 브라우저 닫기 (pytest fixture에서 자동으로 닫기 처리)

@pytest.mark.parametrize("mo_login_fixture", ["mo"], indirect=True)
def test_order_prepack(mo_login_fixture):
    page = mo_login_fixture    # 로그인된 페이지 사용
    # root에서 product_id 읽기
    with open("output\\created_prepack_id.txt", "r") as f:
        product_id = f.read().strip()
    mobile_order_prepack(page, product_id)    # order_prepack 실행