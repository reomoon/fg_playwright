import random # random 함수 추가
from Lib.browser_utils import HighlightPageWrapper
from Lib.common_utils import checkout_process

# Pages/front openpack order
def order_prepack(page, product_prepack_id):

    # allium vendor 페이지로 이동
    page.goto(f"https://beta-www.fashiongo.net/Item/{product_prepack_id}")
    print(f"Navigated to Prepack: {page.url}")
    # 수량 입력 필드 중 하나가 나타날 때까지 대기
    page.wait_for_selector("#txtPkQty0, #txtPkQty1, #txtPkQty2, #txtPkQty3", timeout=10000)

    # 수량을 입력할 locator ID 리스트
    item_qty = [
        'txtPkQty0', # 1번째 수량
        'txtPkQty1', # 2번째 수량
        'txtPkQty2', # 3번째 수량
        'txtPkQty3'  # 4번째 수량
    ]

    item_input = None # item_input 초기화

    # 순서대로 확인하여 가능한 입력 필드 찾기
    for input_id in item_qty:
        item_input = page.locator(f"#{input_id}") # 각 수량에 대한 locator 생성
        if item_input.is_visible() and item_input.is_enabled(): # 입력 필드가 보이고 활성화된 경우
            break   # 입력 필드가 보이고 활성화된 경우 종료 

    # item_input를 찾지 못할 경우 예외 처리
    if not item_input:
        raise Exception("No available item_input field found.")
    
    # item_input으로 찾은 locator에 랜덤값 입력
    random_quantity = random.randint(1,101) # 1 ~ 100 랜덤 값
    item_input.type(str(random_quantity)) # type 랜덤 값 입력

    # Add To Shopping BAG 버튼 클릭
    page.locator('.btn.btn_black_v01.addCart.nclick').click()

    # 페이지 로딩 상태를 기다림
    page.wait_for_load_state('networkidle')

    # 헤더 /cart 아이콘 클릭
    page.locator('#miniCount').click()

    # checkout_process 호출
    checkout_process(page)

    