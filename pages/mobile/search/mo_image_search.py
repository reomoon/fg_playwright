from pathlib import Path

def mobile_image_search(page):
    # 홈 페이지로 이동
    page.goto('https://beta-mobile.fashiongo.net/home', wait_until="domcontentloaded", timeout=60000)
              
    # Top Vendor 팝업 닫기
    dont_show_popup = page.locator('a.link-footer-sub')
    if dont_show_popup.count() > 0 and dont_show_popup.is_visible():
        dont_show_popup.click()
    else:
        top_vendor_close = page.locator('button.popup_cover_close')
        if top_vendor_close.count() > 0 and top_vendor_close.is_visible():
            top_vendor_close.click()

    # 헤더 이미지 버튼 클릭
    header_image_insert = page.locator('button.btn_tool.photo.nclick')
    header_image_insert.click()
    page.wait_for_timeout(1000)

    # 이미지 파일 경로
    current_dir = Path(__file__).parent
    file_path = (current_dir / "top.jpg").resolve()

    print(f"업로드할 이미지 파일 경로: {file_path}")

    if not file_path.exists():
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {file_path}")

    # API 응답 수집
    api_called = False
    api_response_data = None

    def collect_response(response):
        nonlocal api_called, api_response_data
        # api/mobile/image-search/partials?imageUrl=... 형식 감지
        if "api/mobile/image-search/partials" in response.url and "imageUrl=" in response.url:
            # print(f"✅ 이미지 검색 API 감지: {response.url}")
            api_called = True
            try:
                api_response_data = response.json()
                print(f"API 응답 데이터: {api_response_data}")
            except Exception as e:
                print(f"응답 파싱 실패: {e}")

    page.on("response", collect_response)

    # input 요소 대기
    print("input[type='file'] 요소 대기")
    page.wait_for_selector("input[type='file']", state="attached", timeout=30000)
    print("input[type='file'] 요소 확인")

    # ElementHandle로 직접 파일 설정 (hidden이어도 작동)
    file_input_handle = page.query_selector("input[type='file']")
    if file_input_handle is None:
        raise AssertionError("input[type='file'] not found")

    print("파일 업로드 시작")
    file_input_handle.set_input_files(str(file_path))
    print("파일 업로드 완료")

    print("API 응답 대기 중... (파일 S3 업로드 후 API 호출 대기)")
    page.wait_for_timeout(15000)

    # 응답 확인
    if api_called and api_response_data:
        if (
            "data" in api_response_data and
            api_response_data["data"] and
            "searchProvider" in api_response_data["data"] and
            api_response_data["data"]["searchProvider"] in ["AI_FASHION", "RECOMMENDATION"]
        ):
            print(f"✅ 이미지 검색 API 성공 - searchProvider: {api_response_data['data']['searchProvider']}")
        else:
            print(f"❌ 응답 형식 오류: {api_response_data}")
    else:
        print("❌ API 호출 안 됨")

    page.remove_listener("response", collect_response)