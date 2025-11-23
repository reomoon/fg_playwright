def mo_login_home(page, account="mo"):
    def is_trend_report_response(response):
        return "/api/mobile/trendReport/home" in response.url

    with page.expect_response(is_trend_report_response, timeout=30000) as response_info:
        page.goto('https://beta-mobile.fashiongo.net/home')
        
        # 블록 안에서 바로 응답 처리
        response = response_info.value
        if response.status == 200:
            data = response.json()
            d = data.get("data")
            if isinstance(d, list):
                for item in d:
                    if isinstance(item, dict) and item.get("curatedTypeName") == "Trend report":
                        print("🅿 /home API 확인 성공(curatedTypeName: Trend report)")
                        return True
            elif isinstance(d, dict) and d.get("curatedTypeName") == "Trend report":
                print("🅿 /home API 확인 성공(curatedTypeName: Trend report)")
                return True
    
    print("❌ trend Report API 확인 실패")
    return False