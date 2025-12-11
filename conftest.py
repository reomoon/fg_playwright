import sys
import io

# UTF-8 인코딩 설정
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import pytest
import os

# pytest-asyncio 비활성화 (Sync API 사용)
pytest_plugins = ()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # pytest가 각 테스트 함수의 실행 결과를 가져옴
    outcome = yield
    rep = outcome.get_result()
    # 테스트 함수 실행 단계에서 실패한 경우만 처리
    if rep.when == "call" and rep.failed:
        # 여러 fixture 이름 중 실제 page 객체를 가져옴 (실제 객체가 있으면 반환, 없으면 None)
        page = (
            item.funcargs.get("page")              # 일반적으로 사용하는 page fixture
            or item.funcargs.get("front_login_fixture")  # 프론트 로그인 fixture
            or item.funcargs.get("mo_login_fixture")  # 모바일 로그인 fixture
            or item.funcargs.get("va_login_fixture")  # 벤더 어드민 로그인 fixture
            or item.funcargs.get("wa_login_fixture")  # 웹 어드민 로그인 fixture
        )
        if page:
            try:
                # output 폴더 생성 (없으면)
                os.makedirs("output", exist_ok=True)
                # 실패 시 현재 화면을 캡처해서 output 폴더에 저장
                page.screenshot(path=f"output/{item.name}_pytest_fail.png")
                print(f"☑ 캡처 저장: output/{item.name}_pytest_fail.png")
            except Exception as e:
                # 캡처에 실패하면 에러 메시지 출력
                print(f"❌ 스크린샷 실패: {e}")