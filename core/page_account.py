import os
import sys
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 디버깅용 출력 추가(file=sys.stderr 강제 print로 적용여부 확인을 위해 필요)
print("🟡 fr_username =", os.getenv("fr_username"), file=sys.stderr) 
print("🟡 mo_username =", os.getenv("mo_username"), file=sys.stderr)
print("🟡 va_username =", os.getenv("va_username"), file=sys.stderr)
print("🟡 wa_username1 =", os.getenv("wa_username1"), file=sys.stderr)
print("🟡 wa_username2 =", os.getenv("wa_username2"), file=sys.stderr)

# 공통 환경 변수(전역 변수로 정의)
LOGIN_CREDENTIALS = {
    "fr_username": os.getenv("fr_username") or os.getenv("FR_USERNAME"),
    "fr_password": os.getenv("fr_password") or os.getenv("FR_PASSWORD"),
    "va_username": os.getenv("va_username") or os.getenv("VA_USERNAME"),
    "va_password": os.getenv("va_password") or os.getenv("VA_PASSWORD"),
    "mo_username": os.getenv("mo_username") or os.getenv("MO_USERNAME"),
    "mo_password": os.getenv("mo_password") or os.getenv("MO_PASSWORD"),
    "wa_username1": os.getenv("wa_username1") or os.getenv("WA_USERNAME1"),
    "wa_password1": os.getenv("wa_password1") or os.getenv("WA_PASSWORD1"),
    "wa_username2": os.getenv("wa_username2") or os.getenv("WA_USERNAME2"),
    "wa_password2": os.getenv("wa_password2") or os.getenv("WA_PASSWORD2"),
}

# 또는 필수 값들이 없으면 에러 발생
required_vars = [
    "fr_username", "fr_password",
    "va_username", "va_password", 
    "mo_username", "mo_password",
    "wa_username1", "wa_password1",
    "wa_username2", "wa_password2"
]
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {missing_vars}")