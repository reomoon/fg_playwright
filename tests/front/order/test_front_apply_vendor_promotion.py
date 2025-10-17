import pytest
from tests.front.login.test_front_login_fixture import front_login_fixture
from playwright.sync_api import Page
from pages.front.orders.fr_applpy_vendor_promotion import apply_vendor_promotion

def test_apply_vendor_promotion(front_login_fixture: Page):
    page = front_login_fixture  # 로그인된 페이지 사용

    # Vendor Promotion 적용 테스트
    apply_vendor_promotion(page)