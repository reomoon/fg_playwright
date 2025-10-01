import pytest
from tests.web.FR_tests.test_login import login_fixture
from playwright.sync_api import Page
from Pages.web.FR_Pages.orders.Vendor_promotion import apply_vendor_promotion

def test_FR_14_VendorPromotion(login_fixture: Page):
    page = login_fixture  # 로그인된 페이지 사용

    # Vendor Promotion 적용 테스트
    apply_vendor_promotion(page)