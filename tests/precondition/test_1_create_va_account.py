import pytest
from pages.wa.wa_login_token import wa_login_token
from pages.wa.wa_create_va_account import create_vendor_account

def test_create_vendor_account(page):
    """벤더 계정 생성 테스트"""
    # 1. wa_login_token으로 로그인 및 토큰 획득
    page = wa_login_token(page, account="wa2")
    
    # 2. 벤더 계정 생성
    create_vendor_account(page)
