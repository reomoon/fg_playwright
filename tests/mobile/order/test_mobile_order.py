import pytest
from Pages.mobile.MO_Pages.mobile_order_openpack_page import mobile_order_openpack
from Pages.mobile.MO_Pages.mobile_order_prepack_page import mobile_order_prepack
from test_mobile_login import login_fixture

@pytest.mark.parametrize("login_fixture", ["mo"], indirect=True)
def test_order_openpack(login_fixture):
    page = login_fixture    # 로그인된 페이지 사용
    # root에서 product_id 읽기
    with open("created_openpack_id.txt", "r") as f:
        product_id = f.read().strip()
    mobile_order_openpack(page, product_id)    # order_openpack 실행
    # 브라우저 닫기 (pytest fixture에서 자동으로 닫기 처리)

@pytest.mark.parametrize("login_fixture", ["mo"], indirect=True)
def test_order_prepack(login_fixture):
    page = login_fixture    # 로그인된 페이지 사용
    # root에서 product_id 읽기
    with open("created_prepack_id.txt", "r") as f:
        product_id = f.read().strip()
    mobile_order_prepack(page, product_id)    # order_prepack 실행