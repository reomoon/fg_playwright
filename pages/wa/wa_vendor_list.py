from core.page_wrapper import HighlightPageWrapper

def wa_vendor_list(page):
    # 1. is_getvendorlist API 응답을 기다릴 함수 정의
    def is_getvendorlist_response(response):
        # 응답 URL에 '/api/vendor/getvendorlist'가 포함되어 있으면 True 반환
        return "/api/vendor/getvendorlist" in response.url

    # 2. expect_response 블록 안에서 페이지 이동
    with page.expect_response(is_getvendorlist_response, timeout=10000) as response_info:
        page.goto("https://beta-webadmin.fashiongo.net/#/vendor-list")

    # 3. API 응답 객체 가져오기
    response = response_info.value

    # 4. 응답 상태 코드가 200(정상)인지 확인
    if response.status == 200:
        # 5. 응답 데이터를 JSON 형태로 파싱
        data = response.json()
        table = data.get("data", {}).get("Table", [])
        message = data.get("message")
        # 6. table에 값이 하나라도 있으면
        if isinstance(table, list) and len(table) > 0 and message == "success": 
            print(f"🅿 Vendor List에 Table과 message값이 {message} 입니다.")
            return True
        else:
            # table에 값이 없거나 message가 success가 아니면
            print(f"🗙 Vendor List 조건 불충족. Table: {table}, message: {message}")
            return False
    else:
        # 호출 실패하면
        print("❌ /api/vendor/getvendorlist API 호출 실패")
        return False
  