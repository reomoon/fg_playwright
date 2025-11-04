import os
import sys
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 디버깅용 출력 추가(file=sys.stderr 강제 print로 적용여부 확인을 위해 필요)
print("🅰 fr_username =", os.getenv("fr_username"), file=sys.stderr) 
print("🅰 mo_username =", os.getenv("mo_username"), file=sys.stderr)
print("🅰 va_username =", os.getenv("va_username"), file=sys.stderr)
print("🅰 wa1_username =", os.getenv("wa1_username"), file=sys.stderr)
print("🅰 wa2_username =", os.getenv("wa2_username"), file=sys.stderr)

# 공통 환경 변수(전역 변수로 정의)
LOGIN_CREDENTIALS = {
    "fr_username": os.getenv("fr_username") or os.getenv("FR_USERNAME"),
    "fr_password": os.getenv("fr_password") or os.getenv("FR_PASSWORD"),
    "va_username": os.getenv("va_username") or os.getenv("VA_USERNAME"),
    "va_password": os.getenv("va_password") or os.getenv("VA_PASSWORD"),
    "mo_username": os.getenv("mo_username") or os.getenv("MO_USERNAME"),
    "mo_password": os.getenv("mo_password") or os.getenv("MO_PASSWORD"),
    "wa1_username": os.getenv("wa1_username") or os.getenv("WA1_USERNAME"),
    "wa1_password": os.getenv("wa1_password") or os.getenv("WA1_PASSWORD"),
    "wa2_username": os.getenv("wa2_username") or os.getenv("WA2_USERNAME"),
    "wa2_password": os.getenv("wa2_password") or os.getenv("WA2_PASSWORD"),
}

# 또는 필수 값들이 없으면 에러 발생
required_vars = [
    "fr_username", "fr_password",
    "va_username", "va_password", 
    "mo_username", "mo_password",
    "wa1_username", "wa1_password",
    "wa2_username", "wa2_password"
]
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {missing_vars}")