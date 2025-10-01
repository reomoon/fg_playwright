import pytest
from Pages.mobile.search.mobile_search_page import mobile_text_search
from test_mobile_login import login_fixture

@pytest.mark.parametrize("login_fixture", ["mo"], indirect=True)
def test_mobile_text_search(login_fixture):
    page = login_fixture    # 로그인된 페이지 사용
    mobile_text_search(page)
