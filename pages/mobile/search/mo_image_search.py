import json
import re
from pathlib import Path
from core.page_wrapper import create_highlighted_page

def mobile_image_search(page):
    # 홈 페이지로 이동
    page.goto('https://beta-mobile.fashiongo.net/home', wait_until="domcontentloaded", timeout=60000)

    # Top Vendor 팝업의 "Don't show again for 24 hours"가 있으면 클릭, 없으면 닫기 버튼 클릭
    dont_show_popup = page.locator('a.link-footer-sub')
    if dont_show_popup.count() > 0 and dont_show_popup.is_visible():
        dont_show_popup.click()
        print("☑ 'Don't show again for 24 hours' 클릭")
    else:
        top_vendor_close = page.locator('button.popup_cover_close')
        if top_vendor_close.count() > 0 and top_vendor_close.is_visible():
            top_vendor_close.click()
            print("☑ Top Vendor 팝업 닫기 클릭")

    # 헤더 이미지 추가
    header_image_insert = page.locator('button.btn_tool.photo.nclick')
    header_image_insert.click()
    page.wait_for_timeout(1000)  # 충분히 대기

    # 이미지 파일 경로
    current_dir = Path(__file__).parent
    file_path = (current_dir / "top.jpg").resolve()

    print(f"☑ 업로드할 이미지 파일 경로: {file_path}")

    if not file_path.exists():
        print(f"❌ 업로드할 이미지 파일을 찾을 수 없습니다: {file_path}")
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {file_path}")


    # 이미지 검색 API 응답을 기다리면서 파일 업로드
    def is_image_search_response(response):
        # API https://beta-mobile.fashiongo.net/api/mobile/image-search/partials?
        return "api/mobile/image-search/partials" in response.url

    # input[type="file"]가 이미 있으면 바로 사용, 없으면 최대 30초 대기
    try:
        file_input = page.locator('input[type="file"]').first
        if not file_input.count():
            page.wait_for_selector('input[type="file"]', state="attached", timeout=30000)
            file_input = page.locator('input[type="file"]').first
        print("☑ 파일 input 확인")
    except Exception as e:
        print("❌ 파일 input을 찾을 수 없습니다:", e)
        raise

    # 파일 업로드
    file_input.set_input_files(str(file_path))
    print("☑ 파일 업로드 완료, 3초 대기")
    page.wait_for_timeout(3000)

    # 그 다음에 API 응답 대기
    with page.expect_response(is_image_search_response, timeout=30000) as response_info:
        pass  # 여기서는 별도 동작 없이 응답만 기다림

    response = response_info.value
    data = response.json()
    if "data" in data and "searchProvider" in data["data"] and data["data"]["searchProvider"] == "AI_FASHION":
        print("🅿 AI_FASHION으로 불러오기를 성공 하였습니다.(이미지 검색 API 성공)")
    else:
        print("❌ AI_FASHION으로 불러오기를 실패 하였습니다.(이미지 검색 API 실패)")