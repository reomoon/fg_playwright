import pytest
from pages.mobile.MyAccount.mo_add_new_card import mo_add_new_card
from tests.mobile.login.test_mobile_login_fixture import mo_login_fixture

@pytest.mark.parametrize("mo_login_fixture", ["mo"], indirect=True)
def test_mobile_card(mo_login_fixture):
    page = mo_login_fixture
    mo_add_new_card(page)
    