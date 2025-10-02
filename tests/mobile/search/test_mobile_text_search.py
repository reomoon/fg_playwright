import pytest
from pages.mobile.search.mo_search import mobile_text_search
from tests.mobile.login.test_mobile_login_fixture import mo_login_fixture

@pytest.mark.parametrize("mo_login_fixture", ["mo"], indirect=True)
def test_mobile_text_search(mo_login_fixture):
    page = mo_login_fixture    # 로그인된 페이지 사용
    mobile_text_search(page)
