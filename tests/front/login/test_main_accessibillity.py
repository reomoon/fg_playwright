import pytest
from playwright.sync_api import sync_playwright

def test_main_accessibility():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # JS 콘솔 에러 감시 (초기 로드부터 잡도록 먼저 등록)
        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

        # 1️⃣ 페이지 접속
        response = page.goto("https://beta-www.fashiongo.net", wait_until="domcontentloaded", timeout=45000)
        assert response is not None, "❌ 페이지 응답이 없습니다."
        assert response.status == 200, f"❌ HTTP 상태 코드: {response.status}"

        # 2️⃣ 핵심 요소 확인 (예: 로그인 버튼)
        page.wait_for_selector(".guest-main-landing", timeout=10000)
        print("☑ 핵심 요소(게스트 메인 랜딩) 표시 확인됨")

        page.wait_for_selector(".btn-base", timeout=10000)
        print("☑ 핵심 요소(로그인 버튼) 표시 확인됨")

        # 4️⃣ 콘솔 에러 없으면 성공
        assert not errors, f"❌ 콘솔 에러 발생: {errors}"

        print("🅿 메인페이지 접근 성공 ✅")
        browser.close()

        