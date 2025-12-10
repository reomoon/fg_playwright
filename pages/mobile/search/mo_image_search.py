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

    # 파일 input 요소 찾기
    file_input = page.locator('input[type="file"]')

     # 이미지 업로드 직후 모든 response를 수집
    responses = []

    def collect_response(response):
        if "api/mobile/image-search/partials" in response.url:
            print("API 응답 URL:", response.url)
            responses.append(response)

    page.on("response", collect_response)

    # 파일 업로드
    file_input.set_input_files(str(file_path))
    print("☑ 파일 업로드 완료, 10초 대기")
    page.wait_for_timeout(10000)  # 충분히 대기

    # 수집된 응답에서 원하는 결과 찾기
    found = False
    for response in responses:
        try:
            data = response.json()
            # print("API 응답 데이터:", data)
            if (
                "data" in data and
                "searchProvider" in data["data"] and
                data["data"]["searchProvider"] in ["AI_FASHION", "RECOMMENDATION"]
            ):
                print("🅿 이미지 검색 API 성공(AI_FASHION 또는 RECOMMENDATION)")
                found = True
                break
        except Exception as e:
            print("❌ 응답 파싱 실패:", e)

    if not found:
        print("❌ AI_FASHION 또는 RECOMMENDATION으로 불러오기를 실패 하였습니다.(이미지 검색 API 실패)")

    # 이벤트 핸들러 해제 (중복 방지)
    page.remove_listener("response", collect_response)