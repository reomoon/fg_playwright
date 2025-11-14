from core.page_wrapper import HighlightPageWrapper

def display_manager(page):
    # 1. getCalendar API 응답을 기다릴 함수 정의
    def is_calendar_response(response):
        # 응답 URL에 'api/display/getLocations'가 포함되어 있으면 True 반환
        return "api/display/getLocations" in response.url

    # 2. expect_response 블록 안에서 페이지 이동
    with page.expect_response(is_calendar_response, timeout=10000) as response_info:
        page.goto("https://beta-webadmin.fashiongo.net/#/display-manager-list")

    # 3. API 응답 객체 가져오기
    response = response_info.value

    # 4. 응답 상태 코드가 200(정상)인지 확인
    if response.status == 200:
        # 5. 응답 데이터를 JSON 형태로 파싱
        data = response.json()
        # 6. 응답 데이터에 success: True가 있으면 성공 처리
        if data.get("success") is True:
            print("🅿 api/display/getLocations API success: True")
            return True
        else:
            # success 값이 False이거나 없으면 실패 처리
            print(f"❌ api/display/getLocations API success 값이 False 또는 없음: {data.get('success')}")
            return False
    else:
        # 응답 상태 코드가 200이 아니면 실패 처리
        print("❌ api/display/getLocations API 호출 실패")
        return False
    

def display_manager2(page):
    # 1. main-schedule API 응답을 기다릴 함수 정의
    def is_main_schedule_response(response):
        # 응답 URL에 '/api/main-schedule'가 포함되어 있으면 True 반환
        return "/api/main-schedule" in response.url

    # 2. expect_response 블록 안에서 페이지 이동
    with page.expect_response(is_main_schedule_response, timeout=10000) as response_info:
        page.goto("https://beta-webadmin.fashiongo.net/#/display-manager-v2")

    # 3. API 응답 객체 가져오기
    response = response_info.value

    # 4. 응답 상태 코드가 200(정상)인지 확인
    if response.status == 200:
        # 5. 응답 데이터를 JSON 형태로 파싱
        data = response.json()
        # 6. 응답 데이터에 success: True가 있으면 성공 처리
        if data.get("success") is True:
            print("🅿 main-schedule API success: True")
            return True
        else:
            # success 값이 False이거나 없으면 실패 처리
            print(f"❌ main-schedule API success 값이 False 또는 없음: {data.get('success')}")
            return False
    else:
        # 응답 상태 코드가 200이 아니면 실패 처리
        print("❌ main-schedule API 호출 실패")
        return False

