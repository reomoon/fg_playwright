import pytest
from pages.va.va_create_promotion import va_create_promotion
from api_request.promotion_startdate import patch_promotion_start_date
from tests.va.test_va_login_fixture import va_login_fixture

@pytest.mark.parametrize("va_login_fixture", ["va"], indirect=True)  # account 파라미터 설정
@pytest.mark.syncio
async def test_va_create_promotion(va_login_fixture):
    page = va_login_fixture # 로그인된 페이지 사용

    # 1. 프로모션 생성 (비동기)
    discount_id, vendor_id = va_create_promotion(page)

    # 2. fromDate 강제 수정 (동기 함수면 await 필요 없음)
    patch_promotion_start_date(discount_id, vendor_id)