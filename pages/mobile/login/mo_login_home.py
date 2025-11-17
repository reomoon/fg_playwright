from core.page_wrapper import HighlightPageWrapper

# Pages/mobile_login
def mo_login_home(page, account="mo"):
    # trendReport API 응답 대기 함수
    def is_trend_report_response(response):
        return "/api/mobile/trendReport/home" in response.url

    with page.expect_response(is_trend_report_response, timeout=10000) as response_info:
        page.goto('https://beta-mobile.fashiongo.net/home')

    response = response_info.value
    if response.status == 200:
        data = response.json()
        d = data.get("data")
        if isinstance(d, list):
            for item in d:
                if isinstance(item, dict) and item.get("curatedTypeName") == "Trend report":
                    print("🅿 /home API 확인 성공(curatedTypeName: Trend report")
                    return True
            print("🗙 리스트 내에 Trend report 없음")
            return False
        elif isinstance(d, dict):
            if d.get("curatedTypeName") == "Trend report":
                print("🅿 /home API 확인 성공(curatedTypeName: Trend report)")
                return True
            else:
                print(f"🗙 curatedTypeName 값이 다름: {d.get('curatedTypeName')}")
                return False
        else:
            print("🗙 data 타입이 dict나 list가 아님")
            return False
    else:
        print("❌ trendReport API 호출 실패")
        return False