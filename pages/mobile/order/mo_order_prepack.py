import random # 랜덤함수 추가
from core.page_wrapper import create_highlighted_page
from core.page_mobile_common import MO_checkout

# Pages/front openpack order
async def mobile_order_prepack(page, product_prepack_id):

    # openpack item url 이동
    await page.goto(f'https://beta-www.fashiongo.net/Item/{product_prepack_id}')

    # 첫 번째 수량 버튼 클릭
    click_count = random.randint(1,6) # 1~5번 랜덤int(정수)
    plus_btn = page.locator('button.btn_plus.nclick').first # 첫 번째 + 버튼
    for _ in range(click_count):
        await plus_btn.click() # 버튼 클릭
        await page.wait_for_timeout(300) # 대기

    # 수량 클릭 후 충분히 대기
    await page.wait_for_timeout(1000)
    
    print(f"첫 번째 수량 +버튼을 {click_count}번 클릭 하였습니다.")
    
    # Add To Shopping Bag 버튼이 나타날 때까지 대기 후 클릭
    if await page.locator('button.btn-base.black').is_visible():
        await page.locator('button.btn-base.black').click()
    else:
        print("Add To Shopping Bag 버튼을 찾지 못했습니다.")

    # 장바구니 추가 API 응답 감지하는 함수
    def check_add_to_cart_response(response):
        """
        add to cart API 응답인지 확인
        Args:
            response: Playwright의 HTTP 응답 객체
        Returns:
            bool: add-to-cart API이고 POST 요청이면 True, 아니면 False
        """
        return(
            'add-to-cart' in response.url and # URL에 'add-to-cart'가 포함되어 있고
            response.request.method == "POST" # HTTP 메서드가 POST인 경우
        )
    # Add to Shopping Bag 버튼 클릭과 동시에 API 응답 대기
    print("장바구니 추가 중..")
    try:
        # page.expect_response(): 특정 네트워크 응답이 올 때까지 기다리는 Playwright 메서드
        async with page.expect_response(check_add_to_cart_response, timeout=10000) as response_info:
            # with 블록 안에서 실제 액션(버튼 클릭)을 실행
            # 이 클릭으로 인해 add-to-cart API가 호출될 예정
            # page.locator('button.btn_add_bag.nclick', has_text="Add to shopping bag").click()
            # JavaScript로 직접 클릭
            add_bag_button = page.locator('button.btn_add_bag.nclick')
            await add_bag_button.evaluate("el => el.click()")
            print("☑ Add to shopping bag 클릭 성공!")

        # with 블록이 끝나면 API 응답이 response_info.value에 저장됨
        response = await response_info.value

        # HTTP 상태 코드가 200(성공)인지 확인
        if response.status == 200:
            data = await response.json() # JSON 응답을 파싱하여 Python 딕셔너리로 변환
            print(f"장바구니 추가 API 응답: {data}")

            # data.get('success'): 'success' 키가 없으면 None 반환 (KeyError 방지)
            if data.get('success') == True: 
                print("장바구니 추가 응답 성공")
            else:
                print(f"❌ 장바구니 추가 실패:{data}")
        else:
            print(f"❌ HTTP 상태 코드: {response.status}")
    except Exception as e:
        print(f"❌ 장바구니 추가 API 응답 대기 실패:{e}")

    # back 버튼 클릭
    await page.locator('button.btn_back').click()

    # Footer Bag 아이콘 선택
    await page.locator('ion-tab-button span.icon.bag').click()
    print("☑ footer Bag 버튼 클릭 성공")

    # checkout_process 호출
    await MO_checkout(page)