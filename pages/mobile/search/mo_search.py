import random
import asyncio
from core.page_wrapper import create_highlighted_page

async def mobile_text_search(page):
    # 홈 페이지로 이동
    await page.goto('https://beta-mobile.fashiongo.net/home')
    
    # 헤더의 Search 입력란을 찾아 클릭하여 포커스
    header_search_input = page.locator('input[placeholder="Search"]')
    await header_search_input.click()

    # 검색어 후보 리스트에서 랜덤하게 하나 선택
    random_search = ['diamante jeans', 'floral crop top', 'bodycon dress']
    random_text = random.choice(random_search)  # 랜덤 검색어 선택
    await header_search_input.type(random_text, delay=50)  # 검색어 입력 (타이핑 효과)

    result = {"found": False}  # 검색어 일치 여부 결과 저장용

    # 최근 검색어 API 응답을 처리하는 핸들러 함수
    async def handle_response(response):
        # 최근 검색어 API 응답만 처리
        if "api/mobile/keyword/recent-search-history" in response.url:
            try:
                data = await response.json() # JSON → dict로 변환
                print("API 응답:", data)  # 응답 전체 출력
                # data["data"]가 리스트인지 확인
                if isinstance(data.get("data"), list) and data["data"]:
                    # data 리스트에 있는 모든 keyword 출력
                    for item in data["data"]:
                        print(f"검색어(keyword): {item['keyword']}")
                    # 리스트 중 하나라도 random_text와 일치하면 Pass
                    if any(item["keyword"] == random_text for item in data["data"]):
                        print(f"Pass: 검색어가 keyword == {random_text} 값이 일치합니다.")
                        result["found"] = True
                    else:
                        print("Fail: 검색어가 keyword 값과 일치하지 않습니다.")
                else:
                    print("data 리스트가 비어 있거나 리스트가 아님.")
            except Exception as e:
                print(f"API 응답 파싱 오류: {e}")

    # 반드시 검색 버튼 클릭 전에 핸들러를 등록해야 응답을 받을 수 있음
    def on_response(response):
        asyncio.create_task(handle_response(response))
    page.on("response", on_response)
    await page.locator('.btn_search').click()  # 검색 버튼 클릭
    await page.wait_for_timeout(10000)  # 응답 대기 (10초)

    # 더 이상 필요 없으니 핸들러 해제
    page.remove_listener("response", on_response)

    # 결과가 없으면 오류 메시지 출력
    if not result["found"]:
        print("API 응답 오류 또는 데이터 없음")