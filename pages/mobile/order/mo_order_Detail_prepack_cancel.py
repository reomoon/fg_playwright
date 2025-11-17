import random  # 랜덤함수 추가
from core.page_wrapper import create_highlighted_page
from core.page_mobile_common import MO_checkout

# Pages/front openpack order
def mobile_orderDetail_prepack_cancel(page, product_id):

    # openpack item url 이동
    page.goto(f'https://beta-www.fashiongo.net/Item/{product_id}')

    # 첫 번째 수량 버튼 클릭
    click_count = random.randint(1,6) # 1~5번 랜덤int(정수)
    plus_btn = page.locator('button.btn_plus.nclick').first # 첫 번째 + 버튼
    for _ in range(click_count):
        plus_btn.click() # 버튼 클릭
        page.wait_for_timeout(300) # 대기

    # 수량 클릭 후 충분히 대기
    page.wait_for_timeout(1000)
    print(f"첫 번째 수량 +버튼을 {click_count}번 클릭 하였습니다.")
 
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
            else:
                print(f"❌ 장바구니 추가 실패:{data}")
        else:
            print(f"❌ HTTP 상태 코드: {response.status}")
    except Exception as e:
        print(f"❌ 장바구니 추가 API 응답 대기 실패:{e}")

    # back 버튼 클릭
    page.locator('button.btn_back').click()
    page.wait_for_timeout(1000)  # 1초 대기

    # Cart 페이지 이동
    page.goto('https://beta-mobile.fashiongo.net/cart')

    # checkout_process 호출
    MO_checkout(page)

    # PO Number 추출
    PO_number = page.locator('a.link_order').inner_text()
    print(f"☑ PO Number: {PO_number}")

    # Order List 이동
    page.goto("https://beta-mobile.fashiongo.net/order")

    # 해당 PO Number가 있는 리스트 선택
    page.locator('div.po-number > span', has_text=PO_number).click()
    print(f"☑ Order List에서 {PO_number}를 선택했습니다.")

    # 상세 페이지 URL 확인
    expected_url = f"https://beta-mobile.fashiongo.net/order/{PO_number}"
    page.wait_for_url(expected_url, timeout=5000)
    if page.url == expected_url:
        print(f"🅿 Order Info URL이 맞습니다: {page.url}")
    else:
        print(f"❌ 주문 상세 URL 불일치: {page.url} (예상: {expected_url})")

    # Cancel Order 버튼 찾기 및 클릭
    page.wait_for_timeout(3000)
    cancel_order = page.locator('button.link-cancel', has_text="CANCEL ORDER")
    
    # 버튼이 보이고 활성화될 때까지 대기
    cancel_order.wait_for(state='visible', timeout=10000)
    cancel_order.scroll_into_view_if_needed()
    cancel_order.focus()
    page.wait_for_timeout(2000) # 팝업 뜰때까지 대기
    
    # 상태 확인 (디버깅용)
    print(f"is_visible: {cancel_order.is_visible()}")
    print(f"is_enabled: {cancel_order.is_enabled()}")
    
    try:
        # 먼저 일반 클릭 시도
        cancel_order.click(force=True, timeout=5000)
        print("☑ CANCEL ORDER 버튼 클릭 성공")
    except Exception as e:
        print(f"❌ CANCEL ORDER 일반 클릭 실패: {e}")
        # JS로 강제 클릭 시도
        try:
            cancel_order.evaluate("el => el.click()")
            print("☑ CANCEL ORDER 버튼 클릭(JS로 강제 클릭)")
        except Exception as js_e:
            print(f"❌ JS 클릭도 실패: {js_e}")
            page.screenshot(path="output/cancel_order_fail.png")
            return False
    
    # 팝업이 뜰 때까지 충분히 대기 (중요!)
    try:
        # Yes 버튼이 나타날 때까지 대기
        page.wait_for_selector('span.alert-button-inner', timeout=10000)
        print("☑ Cancel Confirmation 팝업이 나타났습니다.")
        
        # Yes 버튼 클릭
        cancel_popup = page.locator('span.alert-button-inner', has_text="Yes")
        cancel_popup.wait_for(state='visible', timeout=5000)
        cancel_popup.click(force=True)
        print("☑ Cancel Confirmation 팝업 Yes 클릭")
    except Exception as e:
        print(f"❌ Cancel Confirmation 팝업 또는 Yes 버튼을 찾지 못했습니다: {e}")
        page.screenshot(path="output/cancel_popup_fail.png")
        return False
    
    # Cancelled 상태 확인
    page.wait_for_timeout(3000)
    cancelled_found = False
    for el in page.locator('div.value').all():
        text = el.inner_text()
        if "Cancelled" in text or "Canceled" in text:
            cancelled_found = True
            break

    if cancelled_found:
        print("🅿 주문이 Canceled 상태로 변경되었습니다.")
        return True
    else:
        print("❌ 주문이 Canceled 상태가 아닙니다.")
        page.screenshot(path="output/cancel_status_fail.png")
        return False


