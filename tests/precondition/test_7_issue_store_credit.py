import os
import json
import pytest
from dotenv import load_dotenv
from tests.va.test_va_login_fixture import va_login_fixture

# .env 로드 (테스트 시작 시 한 번만 실행)
load_dotenv()

SAVE_URL = "https://beta-vendoradmin.fashiongo.net/api/order/saveStoreCredit"


def _extract_va_token(page):
    """로그인된 Vendor Admin 페이지에서 Bearer 토큰을 가져온다."""
    token = page.evaluate("() => localStorage.getItem('token')")
    if token:
        return token

    # 백업: 쿠키에서 토큰 탐색
    for c in page.context.cookies():
        name = c.get("name", "")
        if name in ("VA_SSO_SESSION", "BETA_FG_TOKEN", "FG_TOKEN") and c.get("value"):
            return c["value"]
    return None


def save_store_credit(page, rid: int, reason: str, amount: float):
    token = _extract_va_token(page)
    assert token, "❌ VendorAdmin 토큰을 찾지 못했습니다."

    payload = {"rid": rid, "reason": reason, "amount": amount}
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
    }

    print(f"☑ API URL: {SAVE_URL}")
    print(f"🅰 rid={rid}, reason='{reason}', amount={amount}")

    resp = page.request.post(SAVE_URL, data=json.dumps(payload), headers=headers)
    status = resp.status                 # ✅ () 제거
    text = resp.text()                   # ✅ 메서드는 그대로

    print(f"☑ 응답 상태 코드: {status}")
    print(f"☑ 응답 본문: {text[:500]}...")
    assert 200 <= status < 300, f"❌ API 실패 (status={status})"
    print("🅿 스토어 크레딧 지급 성공")


def test_save_store_credit_api_both(va_login_fixture):
    page = va_login_fixture
    print("☑ va_login_fixture 실행됨 (벤더 어드민 로그인 OK)")

    # 두 환경변수(fr_user_id, fr_user_mobile_id)를 읽어서 각각 스토어 크레딧 지급 테스트
    for env_key, reason, amount in [
        ("fr_user_id", "API test", 200),              
        ("fr_user_mobile_id", "API test (mobile)", 200),  
    ]:
        user_id = os.getenv(env_key)  # .env에서 해당 환경변수 값 읽기
        assert user_id, f"❌ .env 파일에 {env_key}가 없습니다."  # 환경변수 없으면 실패
        user_id_num = user_id.split()[0]  # 공백 앞의 숫자만 추출
        rid = int(user_id_num)  # 문자열을 int로 변환 (API에 넘길 ID)
        save_store_credit(page, rid=rid, reason=reason, amount=amount)  # 실제 API 호출 및 검증