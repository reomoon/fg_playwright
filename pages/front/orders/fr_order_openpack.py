import random # 랜덤함수 추가
from core.page_wrapper import HighlightPageWrapper
from core.page_front_common import checkout_process

# Pages/front openpack order
def order_openpack(page, product_openpack_id):

    # allium vendor 페이지로 이동
    page.goto(f"https://beta-www.fashiongo.net/Item/{product_openpack_id}")
    print(f"Navigated to Openpack: {page.url}")
    # 수량 입력 필드 중 하나가 나타날 때까지 대기
    page.wait_for_selector("#openPackEachSizePc00, #openPackEachSizePc10, #openPackEachSizePc20, #openPackEachSizePc30", timeout=10000) 
        
    # 수량을 입력할 locator ID 리스트 
    item_qty = [
        'openPackEachSizePc00', # 1번째 수량
        'openPackEachSizePc10', # 2번째 수량
        'openPackEachSizePc20', # 3번째 수량
        'openPackEachSizePc30'  # 4번째 수량
    ]

    item_input = None # item_input 초기화
    
    # 순서대로 확인하여 가능한 입력 필드 찾기
    for input_id in item_qty:
        item_input = page.locator(f"#{input_id}") # 각 수량에 대한 locator 생성
        if item_input.is_visible() and item_input.is_enabled(): # 입력 필드가 보이고 활성화된 경우
            break # 입력 필드가 보이고 활성화된 경우 종료

    # item_input를 찾지 못할 경우 예외 처리
    if not item_input:
        raise Exception("No availble item_input field found.")

    # item_input으로 찾은 locator에 랜덤 값 입력
    random_quantity = random.randint(1,101) # 1 ~ 100 랜덤 값
    item_input.type(str(random_quantity)) # type 랜덤 값 입력

    # Add To Shopping BAG 버튼 클릭
    page.locator('.btn.btn_black_v01.addCart.nclick').click()

    # 페이지 로딩 상태를 기다림
    page.wait_for_timeout(5000)

    # 헤더 /cart 아이콘 클릭
    # minicount = page.locator("#miniCount")

    # cart 페이지 이동
    page.goto("https://beta-www.fashiongo.net/cart")

    # checkout_process 호출
    checkout_process(page)

    # 주문번호 확인하여 pass 처리 
    # def check_order(response):
    #     return(
    #         "oid" in response.url and
    #         response.request.method == "POST"
    #     )
    # # XHR 응답을 기다리기 위해 expect_response 사용
    # with page.expect_response(check_order) as resp_info:
    #     # 이 블록 안에서 네트워크 요청이 발생해야 함
    #     page.locator('button.order').click()

    # response = resp_info.value # 응답 객체
    # print("주문응답:", response.url)