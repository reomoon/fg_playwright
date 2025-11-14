import pytest
from pages.wa.wa_display_manager import display_manager, display_manager2
from tests.wa.test_wa_login_fixture import wa_login_fixture

@pytest.mark.parametrize("wa_login_fixture", ["wa2"], indirect=True)  # account 파라미터 설정
def test_wa_display_manager(wa_login_fixture):
    page = wa_login_fixture    # 로그인된 페이지 사용
    display_manager(page)


@pytest.mark.parametrize("wa_login_fixture", ["wa2"], indirect=True)  # account 파라미터 설정
def test_wa_display_manager2(wa_login_fixture):
    page = wa_login_fixture    # 로그인된 페이지 사용
    display_manager2(page)
