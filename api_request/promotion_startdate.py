import pytest
from datetime import datetime
import aiohttp
import uuid

# QA 전용 PATCH API를 호출하여 프로모션의 시작일(fromDate)을 오늘 날짜로 강제로 수정하는 함수
async def patch_promotion_start_date(promotion_id: int, vendor_id: int):
    # QA 서버용 PATCH API 엔드포인트
    url = "http://10.230.40.7:17301/v1.0/qa/vendors/promotion/from-date"

    # 오늘 날짜를 yyyy-MM-dd 포맷 문자열로 생성 (예: '2025-07-24')
    today_str = datetime.today().strftime("%Y-%m-%d")

    # 요청 헤더 구성
    headers = {
        # QA 시스템에서 사용하는 고정 어플리케이션 타입
        "Referer-Application-Type": "fashiongo-api-dev",

        # 각 요청마다 고유 식별자 (에러 추적용), UUID 랜덤 생성
        "Request-Id": str(uuid.uuid4()),

        # 사용자 정보 (QA에서 미리 등록된 사용자 값, JSON 형식 문자열)
        "User-Info": '{"userId":"aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "username":"fashiongo-api-dev"}',

        # 대상 벤더 ID (정수형을 문자열로 변환)
        "Vendor-Id": str(vendor_id)
    }

    # 쿼리 스트링 파라미터 (주소 뒤에 붙는 ?fromDate=xxx&promotionId=xxx)
    params = {
        "promotionId": promotion_id,  # 수정할 프로모션 ID
        "fromDate": today_str         # 강제로 바꿀 시작일 (오늘)
    }

    # PATCH 요청 보내기 (aiohttp 사용)
    async with aiohttp.ClientSession() as session:
        async with session.patch(url, headers=headers, params=params) as response:
            status = response.status
            text = await response.text()

            # 결과 확인 (200 또는 204면 성공)
            if status in [200, 204]:
                print(f"[성공] Discount {promotion_id} fromDate → {today_str}")
            else:
                # 실패 시 상태 코드 및 에러 메시지 출력
                print(f"[실패] PATCH 요청 실패: {status} / {text}")