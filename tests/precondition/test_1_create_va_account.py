import pytest
from pages.wa.wa_create_va_account import create_vendor_account
from tests.wa.test_wa_login_fixture import wa_login_fixture

@pytest.mark.parametrize("wa_login_fixture", ["wa2"], indirect=True)  # account 파라미터 설정
def test_create_vendor_account(wa_login_fixture):
    page = wa_login_fixture    # 로그인된 페이지 사용
    create_vendor_account(page)    # Group Manager 권한주기 함수 호출
    # 브라우저 닫기 (pytest fixture에서 자동으로 닫기 처리)