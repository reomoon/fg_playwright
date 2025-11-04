from playwright.sync_api import Page
from core.page_wrapper import HighlightPageWrapper

def Text_search(page: Page, search_text: str):
    # 1. 검색창 클릭
    search_input = page.locator('.search-input')
    search_input.click()

    # 2. 텍스트 입력
    search_input.fill(search_text)

    # 3. 검색 버튼 클릭
    search_button = page.locator('.btn-search')
    search_button.click()

    # 4. 검색 결과가 로딩될 때까지 대기 (예: 'a.item.nclick'이 나타날 때까지)
    page.wait_for_selector('a.item.nclick')

    # 5. 검색 결과 목록에서 텍스트가 포함된 항목이 있는지 확인
    item_names = page.locator('a.item.nclick').all_text_contents()

    # 6. 결과 확인 및 로그 출력
    matched = any(search_text.lower() in name.lower() for name in item_names)
    if matched:
        print(f"[검색 성공] '{search_text}'가 포함된 항목이 검색됨.")
    else:
        print(f"[검색 실패] '{search_text}'가 포함된 항목이 검색되지 않음.")