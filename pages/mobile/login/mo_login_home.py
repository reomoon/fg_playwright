def mo_login_home(page, account="mo"):
    def is_trend_report_response(response):
        return "/api/mobile/trendReport/home" in response.url

    # wait_for_response는 async API에서만 사용 가능, sync API에서는 page.expect_response를 사용해
    with page.expect_response(is_trend_report_response, timeout=60000) as response_info:
        page.goto('https://beta-mobile.fashiongo.net/home', wait_until="domcontentloaded")
    try:
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
    except Exception as e:
        print(f"❌ trend Report API 확인 실패: {e}")
        return False

    print("❌ trend Report API 확인 실패")
    return False