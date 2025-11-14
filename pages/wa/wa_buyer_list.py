from core.page_wrapper import HighlightPageWrapper

def wa_buyer_list(page):
    # 1. is_admin_retailer_response API 응답을 기다릴 함수 정의
    def is_admin_retailer_response(response):
        # 응답 URL에 '/api/buyer/getadminretailer'가 포함되어 있으면 True 반환
        return "/api/buyer/getadminretailer" in response.url

    # 2. expect_response 블록 안에서 페이지 이동
    with page.expect_response(is_admin_retailer_response, timeout=10000) as response_info:
        page.goto("https://beta-webadmin.fashiongo.net/#/buyer-list")

    # 3. API 응답 객체 가져오기
    response = response_info.value

    # 4. 응답 상태 코드가 200(정상)인지 확인
    if response.status == 200:
        # 5. 응답 데이터를 JSON 형태로 파싱
        data = response.json()
        table = data.get("data", {}).get("Table", [])
        # 6. table에 값이 하나라도 있으면
        if isinstance(table, list) and len(table) > 0: 
            print("🅿 Buyer List에 Table 값이 있습니다.")
            return True
        else:
            # table에 값이 없으면
            print("❌ Buyer List에 Table 값이 없습니다.")
            return False
    else:
        # 호출 실패하면
        print("❌ /api/buyer/getadminretailer API 호출 실패")
        return False
  