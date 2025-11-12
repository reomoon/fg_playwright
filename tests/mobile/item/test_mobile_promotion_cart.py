import pytest
from pages.mobile.item.mo_AddtoCart import mobile_add_to_cart_openpack
from pages.mobile.item.mo_promotion_cart import mobile_promotion_cart
from tests.mobile.login.test_mobile_login_fixture import mo_login_fixture

@pytest.mark.parametrize("mo_login_fixture", ["mo"], indirect=True)
def test_promotion_cart(mo_login_fixture):
    page = mo_login_fixture    # 로그인된 페이지 사용
    # root에서 product_id 읽기
    with open("openpack_productid.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]
        product_id = lines[-1] if lines else ""
    print(f"☑ item productId: {product_id}")
    mobile_add_to_cart_openpack(page, product_id)  
    mobile_promotion_cart(page)  
    