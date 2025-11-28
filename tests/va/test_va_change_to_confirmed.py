import pytest
from playwright.sync_api import Page
from tests.va.test_va_login_fixture import va_login_fixture
from pages.va.va_change_to_confirmed import open_first_new_order_detail
from pages.va.va_change_to_confirmed import change_order_status_to_confirmed

def test_va_change_to_confirmed(va_login_fixture: Page):
    """벤더 어드민 로그인 후 Item List 페이지에서 Active / Inactive Items 섹션 노출 테스트"""
    page = va_login_fixture  # 로그인 완료된 페이지
    print("☑ va_login_fixture 실행됨 (벤더 어드민 로그인 OK)")

    open_first_new_order_detail(page)

    change_order_status_to_confirmed(page)