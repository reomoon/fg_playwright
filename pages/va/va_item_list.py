import pytest
import re
from playwright.sync_api import Page


def item_list_active_inactive_sections(page):

    # 1. 사이드 메뉴에서 'Items' 메뉴 클릭해서 하위 메뉴 펼치기
    print("☑ 'Items' 메인 메뉴 찾기")
    items_menu = page.locator('div.nav__item__title', has_text="Items")
    items_menu.wait_for(state="visible", timeout=10000)
    print("🅿 'Items' 메인 메뉴 표시 확인")

    items_menu.click()
    print("☑ 'Items' 메인 메뉴 클릭 (하위 메뉴 펼치기)")

    # 2. 하위 메뉴에서 'Item List' 메뉴 클릭
    print("☑ 'Item List' 하위 메뉴 찾기")
    item_list_link = page.locator('a.nav__group__item__title', has_text="Item List")
    item_list_link.wait_for(state="visible", timeout=10000)
    print("🅿 'Item List' 하위 메뉴 표시 확인")

    item_list_link.click()
    print("☑ 'Item List' 메뉴 클릭 (Item List 페이지 이동)")

    # 페이지 로드 대기 (네트워크 요청이 어느 정도 끝났는지 기준)
    # page.wait_for_load_state("networkidle")

    # (선택) URL 확인: #/item/editall 로 이동했는지
    current_url = page.url
    print(f"☑ 현재 URL: {current_url}")
    assert "item/editall" in current_url, "❌ Item List URL로 이동하지 않았습니다."

    print("☑ 'Active Items' 패널 타이틀 찾기 (.first 사용)")
    active_header = page.locator("div.panel__header__title").filter(
        has_text="Active Items"
    ).first
    active_header.wait_for(state="visible", timeout=10000)
    assert active_header.is_visible(), "❌ Active Items 패널이 보이지 않습니다."
    print("🅿 'Active Items' 패널 노출 확인")

    print("☑ 'Inactive Items' 패널 타이틀 찾기 (.first 사용)")
    inactive_header = page.locator("div.panel__header__title").filter(
        has_text="Inactive Items"
    ).first
    inactive_header.wait_for(state="visible", timeout=10000)
    assert inactive_header.is_visible(), "❌ Inactive Items 패널이 보이지 않습니다."
    print("🅿 'Inactive Items' 패널 노출 확인")