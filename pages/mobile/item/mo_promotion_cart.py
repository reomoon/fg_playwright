import random  # 랜덤함수 추가
from core.page_wrapper import create_highlighted_page
from core.page_mobile_common import MO_checkout
from api_request.promotion_startdate import patch_promotion_start_date

# Precondition test_4_create_va_promotion 실행
# mobile add to cart openpack
def mobile_add_to_cart_openpack(page, product_id):

    # openpack item url 이동
    page.goto(f'https://beta-www.fashiongo.net/Item/{product_id}')

    # 수량 버튼이 나타날 때까지 대기
    page.wait_for_selector('.btn_openPack', timeout=10000)

    # 옵션 선택
    page.locator('.btn_openPack').first.click()
    
    # 1번째칸 수량 
    item_input1 = page.locator('input.num_input.ng-untouched.ng-pristine.ng-valid')
    random_quantity = random.randint(1, 101)  # 1 ~ 100 랜덤값
    item_input1.first.type(str(random_quantity))  # type 랜덤값 입력
    page.wait_for_timeout(2000)  # 2초 대기
    
    # Add To Shopping Bag 버튼이 나타날 때까지 대기 후 클릭
    if page.locator('button.btn-base.black').is_visible():
        page.locator('button.btn-base.black').click()
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
        return (
            'add-to-cart' in response.url and  # URL에 'add-to-cart'가 포함되어 있고
            response.request.method == "POST"  # HTTP 메서드가 POST인 경우
        )

    # Add to Shopping Bag 버튼 클릭과 동시에 API 응답 대기
    print("장바구니 추가 중..")
    try:
        # page.expect_response(): 특정 네트워크 응답이 올 때까지 기다리는 Playwright 메서드
        with page.expect_response(check_add_to_cart_response, timeout=10000) as response_info:
            # with 블록 안에서 실제 액션(버튼 클릭)을 실행
            # 이 클릭으로 인해 add-to-cart API가 호출될 예정
            # page.locator('button.btn_add_bag.nclick', has_text="Add to shopping bag").click()
            # JavaScript로 직접 클릭
            add_bag_button = page.locator('button.btn_add_bag.nclick')
            add_bag_button.evaluate("el => el.click()")
            print("☑ Add to shopping bag 클릭 성공!")

        # with 블록이 끝나면 API 응답이 response_info.value에 저장됨
        response = response_info.value

        # HTTP 상태 코드가 200(성공)인지 확인
        if response.status == 200:
            data = response.json()  # JSON 응답을 파싱하여 Python 딕셔너리로 변환
            print(f"장바구니 추가 API 응답: {data}")

            # data.get('success'): 'success' 키가 없으면 None 반환 (KeyError 방지)
            if data.get('success') == True: 
                print("장바구니 추가 응답 성공")
                page.wait_for_timeout(1000)
            else:
                print(f"❌ 장바구니 추가 실패:{data}")
        else:
            print(f"❌ HTTP 상태 코드: {response.status}")
    except Exception as e:
        print(f"❌ 장바구니 추가 API 응답 대기 실패:{e}")

# Cart에서 프로모션 선택 
def mobile_promotion_cart(page):
    # Cart 페이지 이동
    page.goto('https://beta-mobile.fashiongo.net/cart')

    # Promotion 선택
    page.locator('.cart-order__promo').click() # Select Promotion 드롭다운 클릭
    page.locator('label.radio').first.click(force=True) # 첫 번째 프로모션의 텍스트 라벨 클릭
    page.locator('.btn-row').click() # Apply Promotion 클릭

    # 할인 전 금액 추출
    sale_price_text = page.locator('em.sale-price').inner_text()  # "$2,574.00"
    sale_price = float(sale_price_text.replace("$", "").replace(",", ""))
    print(f"할인 전 금액: {sale_price}")

    # 할인 금액 추출
    saved_text = page.locator('span.total-saved', log_if_not_found=False).inner_text()    # "Saved $286.00"
    saved_amount = float(saved_text.replace("Saved $", "").replace(",", ""))
    print(f"할인금액: {saved_text}")

    # 할인 후 금액 추출
    total_money_text = page.locator('div.col.total-money').inner_text()  # "... $2,574.00"
    print(f"할인 후 금액: {total_money_text}")
    # 마지막 $금액만 추출
    import re
    match = re.findall(r"\$[\d,]+\.\d{2}", total_money_text)
    if match:
        total_money = float(match[-1].replace("$", "").replace(",", ""))
    else:
        total_money = None

    # 할인 계산
    expected_saved = round(sale_price * 0.10, 2)
    expected_total = round(sale_price - expected_saved, 2)

    # 결과 판정
    if abs(saved_amount - expected_saved) < 0.01 and abs(total_money - expected_total) < 0.01:
        print(f"🅿 할인금액 및 최종금액이 일치합니다. (할인: ${saved_amount}, 최종: ${total_money})")
    else:
        print(f"❌ 할인 계산 불일치. (예상 할인: ${expected_saved}, 실제 할인: ${saved_amount}, 예상 최종: ${expected_total}, 실제 최종: ${total_money})")