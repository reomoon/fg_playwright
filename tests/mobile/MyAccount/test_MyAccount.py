import pytest
from pages.mobile.MyAccount.mo_myaccount_home import mobile_myaccount
from tests.mobile.login.test_mobile_login_fixture import mo_login_fixture

@pytest.mark.parametrize("mo_login_fixture", ["mo"], indirect=True)
def test_mobile_MyAccount(mo_login_fixture):
    page = mo_login_fixture
    mobile_myaccount(page)
    