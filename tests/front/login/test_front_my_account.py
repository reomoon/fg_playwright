import re
import pytest
from playwright.sync_api import Page
from tests.front.login.test_front_login_fixture import front_login_fixture

def test_my_account_home(front_login_fixture):
    page = front_login_fixture  # ✅ 로그인 완료된 페이지

    # 1 아바타('QT') 클릭 → 드롭다운 열기
    print("☑ My Account 아바타(프로필) 버튼 찾기")
    avatar_sel = 'a.user-avatar.nclick[data-nclick-name="site.menu.myaccount"]'
    page.wait_for_selector(avatar_sel, timeout=5000)
    page.locator(avatar_sel).first.click()
    print("☑ 아바타 클릭 완료 (드롭다운 오픈)")

    # 2️ 드롭다운에서 'My Account' 항목 클릭
    print("☑ 드롭다운 내 'My Account' 링크 찾기")
    my_account_link = 'a[href="/MyAccount"]'
    page.wait_for_selector(my_account_link, timeout=5000)
    page.locator(my_account_link).first.click()
    print("☑ 'My Account' 클릭 완료")

    # 3️ 페이지 로드 대기
    page.wait_for_load_state("domcontentloaded")

    # 4️ 상단 타이틀 'My Account Home' 확인
    print("☑ 상단 타이틀 텍스트 확인")
    title_sel = 'span.hx_myac'
    page.wait_for_selector(title_sel, timeout=15000)
    title_text = page.locator(title_sel).inner_text().strip()
    assert title_text == "My Account Home", f"❌ 타이틀 텍스트 불일치: {title_text}"
    print("🅿 'My Account Home' 텍스트 확인")

    # 5️ 최근 주문 영역 H2 존재 확인
    print("☑ 'Your Recent Orders' 섹션 헤더 확인")
    recent_orders_h2 = page.get_by_role(
        "heading",
        name=re.compile(r"^Your Recent Orders", re.I)
    )
    recent_orders_h2.wait_for(timeout=15000)
    assert "Your Recent Orders" in recent_orders_h2.inner_text().strip(), "❌ 'Your Recent Orders' 헤더 텍스트 불일치"
    print("🅿 'Your Recent Orders' 헤더 확인")
 
    print("🅿 My Account 홈 정상 노출 확인 완료 ✅")