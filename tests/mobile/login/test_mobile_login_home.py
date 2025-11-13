import pytest
from pages.mobile.login.mo_login_home import mo_login_home
from tests.mobile.login.test_mobile_login_fixture import mo_login_fixture

@pytest.mark.parametrize("mo_login_fixture", ["mo"], indirect=True)
def test_mobile_login_home(mo_login_fixture):
    page = mo_login_fixture    # 로그인된 페이지 사용
    mo_login_home(page)
