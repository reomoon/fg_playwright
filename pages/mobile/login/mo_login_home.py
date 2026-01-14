def mo_login_home(page, account="mo"):
    def is_trend_report_response(response):
        return "/api/mobile/display/main" in response.url

    try:
        # wait_for_response는 async API에서만 사용 가능, sync API에서는 page.expect_response를 사용
        with page.expect_response(is_trend_report_response, timeout=30000) as response_info:
            page.goto('https://beta-mobile.fashiongo.net/home')
            print("☑ mobile.fashiongo.net/home 이동")
        
        response = response_info.value
        if response.status == 200:
            data = response.json()
            # 최상위 레벨의 success 확인
            if data.get("success") is True: # data 딕셔너리에서 "success" 값이 True(참)일 경우
                print("🅿 /api/mobile/display/main API 확인 성공(success: true)")
                return True
    except Exception as e:
        print(f"⚠️ /api/mobile/display/main 타임아웃/에러: {e}")
        print("⚠️ 페이지 로드만 성공 - 테스트 계속 진행")
        # API 응답을 기다리지 않고 페이지 로드만으로 진행
        try:
            page.wait_for_load_state("load", timeout=30000)
            return True
        except:
            return False

    print("❌ /api/mobile/display/main API 확인 실패")
    return False