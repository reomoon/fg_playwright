import pytest
from playwright.sync_api import Page
from tests.va.test_va_login_fixture import va_login_fixture
from pages.va.va_banner_manager import va_upload_banner_and_submit

def test_va_banner_logo_upload_and_submit(va_login_fixture: Page):
    """벤더 어드민 로그인 후 Banner Manager에서 Logo 업로드 및 Submit 테스트"""
    page = va_login_fixture  # 로그인 완료된 페이지
    print("☑ va_login_fixture 실행됨 (벤더 어드민 로그인 OK)")

    va_upload_banner_and_submit(page)