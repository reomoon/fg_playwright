import pytest
from pages.wa.wa_buyer_list import wa_buyer_list
from tests.wa.test_wa_login_fixture import wa_login_fixture

@pytest.mark.parametrize("wa_login_fixture", ["wa2"], indirect=True)  # account 파라미터 설정
def test_wa_buyer_list(wa_login_fixture):
    page = wa_login_fixture    # 로그인된 페이지 사용
    wa_buyer_list(page)