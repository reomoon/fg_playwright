import sys
import io
import os

# UTF-8 인코딩 설정
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Windows에서 asyncio 이벤트 루프 정책 설정
if sys.platform == 'win32':
    import asyncio
    # Playwright의 greenlet과 호환되는 정책 사용
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import pytest

# pytest-asyncio 비활성화 (Sync API 사용)
pytest_plugins = ()

def pytest_runtest_makereport(item, call):
    """테스트 실패 시 스크린샷 캡처"""
    if call.when == "call" and call.excinfo is not None:
        page = (
            item.funcargs.get("page")
            or item.funcargs.get("front_login_fixture")
            or item.funcargs.get("mo_login_fixture")
            or item.funcargs.get("va_login_fixture")
            or item.funcargs.get("wa_login_fixture")
        )
        if page:
            try:
                os.makedirs("output", exist_ok=True)
                page.screenshot(path=f"output/{item.name}_pytest_fail.png")
                print(f"☑ 캡처 저장: output/{item.name}_pytest_fail.png")
            except Exception as e:
                print(f"❌ 스크린샷 실패: {e}")