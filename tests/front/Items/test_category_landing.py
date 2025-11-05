import re
import pytest
from playwright.sync_api import Page, TimeoutError as PWTimeoutError
from tests.front.login.test_front_login_fixture import front_login_fixture

def test_womens_category_page(front_login_fixture):
    page = front_login_fixture  # 로그인 완료된 페이지

    # 1) GNB에서 Women's Apparel 클릭 (정확 셀렉터 사용)
    print("☑ GNB 'Women's Apparel' 링크 찾기")
    gnb_sel = 'a.nclick[href="/Category/womens-apparel"]'
    page.wait_for_selector(gnb_sel, timeout=5000)
    page.locator(gnb_sel).first.click()
    print("☑ 'Women's Apparel' 클릭")

    # (보강) /Category 또는 /Catalog 경로로 로딩될 수 있어 둘 다 허용
    # page.wait_for_url(re.compile(r"https://[^/]+/(Category|Catalog)/womens-apparel(?:/.*)?"), timeout=10000)
    page.wait_for_load_state("domcontentloaded")
    # page.wait_for_load_state("networkidle")

    # 2) 상단 타이틀 'Women's Apparel' 확인
    print("☑ 상단 타이틀 텍스트 확인")
    title_sel = 'span[name="categories-note"]'
    page.wait_for_selector(title_sel, timeout=5000)
    assert page.locator(title_sel).inner_text().strip() == "Women's Apparel", "❌ 타이틀 텍스트가 일치하지 않습니다."
    print("🅿 'Women's Apparel' 텍스트 확인")

    # 3) 서브카테고리(스와이퍼) 요소 확인
    print("☑ 서브카테고리(슬라이드) 요소 확인")
    slide_sel = '.item-swiper-area .swiper-slide'
    page.wait_for_selector(slide_sel, timeout=5000)
    slide_count = page.locator(slide_sel).count()
    assert slide_count > 0, f"❌ 서브카테고리 슬라이드가 0개입니다. URL: {page.url}"

    # (보강) 유효한 서브카테고리 링크가 붙어 있는지 확인 (Catalog 경로 기준)
    link_sel = '.item-swiper-area .swiper-slide a[href^="/Catalog/womens-apparel/"]'
    valid_link_cnt = page.locator(link_sel).count()
    assert valid_link_cnt > 0, "❌ '/Catalog/womens-apparel/' 링크가 포함된 서브카테고리를 찾지 못했습니다."

    # (보강) 타이틀 h4 존재
    title_h4_sel = '.item-swiper-area h4.item-ttl'
    assert page.locator(title_h4_sel).count() > 0, "❌ 서브카테고리 타이틀(h4.item-ttl)을 찾지 못했습니다."

    print(f"🅿 서브카테고리 슬라이드 {slide_count}개, 유효 링크 {valid_link_cnt}개 확인")

    # 4) 전체 스크린샷 저장
    page.screenshot(path="screens/womens_category.png", full_page=True)
    print("🅿 페이지 정상 노출 확인 완료")