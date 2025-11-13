from core.page_wrapper import HighlightPageWrapper

# Pages/mobile
def mo_category_check(page):
    # 확인할 카테고리 이름과 URL 일부를 리스트로 정의 예) api data categoryName: "Bags", URL /{bags}
    categories = [
        ("Women's Apparel", "womens-apparel"),
        ("Shoes", "shoes"),
        ("Bags", "bags"),
        ("Jewelry", "jewelry"),
        ("Accessories", "accessories"),
        ("Beauty", "beauty"),
        ("Men", "men"),
        ("Kids & Baby", "kids-baby"),
        ("Home", "home"),
        ("Lifestyle", "lifestyle"),
        ("Retailer Supplies", "retailer-supplies"),
    ]

    # 각 카테고리에 대해 반복
    for category_name, url_part in categories:
        # 해당 카테고리의 API 응답을 기다리는 함수 정의
        def is_category_response(response):
            # 응답 URL에 카테고리명이 포함되어 있는지 확인
            return f"/api/mobile/categories/{url_part}" in response.url

        # API 응답을 기다리면서 해당 카테고리 페이지로 이동
        with page.expect_response(is_category_response, timeout=10000) as response_info:
            # 카테고리 페이지로 이동 (예: /category/shoes)
            page.goto(f'https://beta-mobile.fashiongo.net/category/{url_part}')

        # API 응답 객체 가져오기
        response = response_info.value
        if response.status == 200:
            # 응답에서 JSON 데이터 추출
            data = response.json()
            # data 키의 값을 d에 저장 (카테고리 정보)
            d = data.get("data")
            # d가 딕셔너리이고, categoryName이 기대한 값과 같은지 확인
            if isinstance(d, dict) and d.get("categoryName") == category_name:
                print(f"🅿 카테고리 API 확인 성공(categoryName: {category_name})")
            else:
                # categoryName이 다르거나 데이터 구조가 다를 때
                print(f"❌ categoryName 값이 다름: {d.get('categoryName') if isinstance(d, dict) else d}")
        else:
            # API 호출이 실패했을 때
            print(f"❌ 카테고리 API 호출 실패: {category_name}")