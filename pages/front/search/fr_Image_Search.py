from playwright.sync_api import Page
from core.page_wrapper import HighlightPageWrapper
from pathlib import Path
import os


def Image_search(page: Page):
    # 1. 카메라 버튼 클릭 (이미지 검색 모드 진입)
    print("☑ 카메라 버튼(.btn_camera) 클릭 시도")
    search_button = page.locator(".btn_camera")
    search_button.click()
    print("🅿 카메라 버튼 클릭 완료")

    # 2. fr_Image_Search.py 파일이 있는 폴더 기준으로 jeans.jpg 상대 경로 설정
    current_dir = Path(__file__).parent
    file_path = (current_dir / "jeans.jpg").resolve()

    if not file_path.exists():
        print(f"❌ 업로드할 이미지 파일을 찾을 수 없습니다: {file_path}")
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {file_path}")

    print(f"☑ 상대 경로로 찾은 파일: {file_path}")

    # 3. #search_file input 요소가 DOM에 attach 될 때까지 대기
    print("☑ #search_file input attach 대기")
    page.wait_for_selector("#search_file", state="attached", timeout=30000)
    print("🅿 #search_file input attach 확인")

    # 4. ElementHandle 로 직접 input 요소를 잡아서 파일 업로드 실행
    file_input_handle = page.query_selector("#search_file")
    if file_input_handle is None:
        print("❌ #search_file input 요소를 찾지 못했습니다.")
        raise AssertionError("#search_file input not found")

    file_input_handle.set_input_files(str(file_path))
    print("🅿 이미지 파일 업로드 완료")

    # 5. 검색 결과가 로딩될 때까지 대기 (예: 'a.item.nclick' 이 나올 때까지)
    print("☑ 검색 결과 요소('a.item.nclick') 대기")
    page.wait_for_selector("a.item.nclick", timeout=30000)
    print("🅿 검색 결과 요소 확인")

    # 6. 검색 결과 목록 텍스트 수집
    item_names = page.locator("a.item.nclick").all_text_contents()

    # 7. 결과 중 'denim' 혹은 'jean' 이 포함된 항목 필터링
    matching_items = [
        name for name in item_names
        if "denim" in name.lower() or "jean" in name.lower()
    ]

    # 8. 검색 결과 검증 및 로그 출력
    if matching_items:
        print("🅿 이미지 검색 성공, 매칭된 항목:")
        for name in matching_items:
            print("  -", name)
    else:
        print("❌ 이미지 검색 실패: denim/jean 이 포함된 결과가 없습니다.")
    
