from playwright.sync_api import Page
from core.page_wrapper import HighlightPageWrapper
from pathlib import Path
import os

def Image_search(page: Page):

    # 1. 카메라 버튼 클릭
    search_button = page.locator('.btn_camera')
    search_button.click()

    # 2. 업로드 버튼 클릭
    upload_button = page.locator('.inputfile')
    upload_button.click()

    # 3. 청바지 이미지 파일 업로드 (본인 컴퓨터에 맞는 절대경로로 입력 필수)
    file_path = Path("C:/playwrightauto/autoplay/Pages/web/FR_Pages/Search/jeans.jpg").resolve()

    page.click("#search_file")
    page.set_input_files("#search_file", file_path)
    # page.set_input_files('input[type="file"]', file_path)

    # 4. 검색 결과가 로딩될 때까지 대기 (예: 'a.item.nclick'이 나타날 때까지)
    page.wait_for_selector('a.item.nclick')

    # 5. 검색 결과 목록에서 Jeans 혹은 Denim이 포함된 항목이 있는지 확인
    item_names = page.locator('a.item.nclick').all_text_contents()

    # 6. 결과 확인 및 로그 출력
    matching_items = [name for name in item_names if "denim" in name.lower() or "jean" in name.lower()]
    if matching_items:
        print("검색 성공:", matching_items)
    else:
        print("검색 실패")
    
