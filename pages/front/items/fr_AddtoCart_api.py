import json
import requests

# ✅ 1. productid.txt에서 마지막 productId 읽기
def get_last_product_id(filepath="prepack_productid.txt"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.read().strip().splitlines()
            if not lines:
                raise ValueError("파일은 있지만 내용이 비어 있습니다.")
            last_id = lines[-1].strip()
            print(f"🅿 [마지막 상품ID 읽기 성공] {last_id}")
            return last_id
    except FileNotFoundError:
        print("❌ [prepack_productid.txt 없음] 먼저 상품 생성 테스트를 실행해야 합니다.")
        return None
    except Exception as e:
        print(f"❌ [상품ID 읽기 실패] {e}")
        return None


# ✅ 2. 쿠키를 헤더로 변환
def get_cookie_header_from_page(page):
    cookies = page.context.cookies()
    return "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])


# ✅ 3. 장바구니 추가 함수
def add_item_to_cart(page):
    # Step 1: 마지막 productId 읽기
    product_id = get_last_product_id()
    if not product_id:
        print("❌ [상품ID 없음] 장바구니 테스트 중단")
        return False

    # Step 2: Playwright 세션 쿠키 가져오기
    cookie_header = get_cookie_header_from_page(page)

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/json; charset=UTF-8",
        "Origin": "https://beta-www.fashiongo.net",
        "Referer": f"https://beta-www.fashiongo.net/item/{product_id}",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0",
        "Cookie": cookie_header,
    }

    # Step 3: API 요청에 사용할 payload 생성
    payload = {
        "wholeSalerId": "16502",   # allium vendor ID
        "retailerId": "566735",    # 테스트용 retailer ID
        "productId": product_id,   # ✅ 새로 추가된 productId
        "sizeId": "48551",         # 상품 생성 시 사용한 sizeId와 동일
        "colorPacks": [
            {
                "id": "0",
                "colorId": "893825",        # RED
                "colorName": "RED",
                "qty": ["5", "5", "5", "0", "0", "0", "0", "0", "0", "0", "15"],
                "pkQty": "5",
                "unitPrice": "22",
                "isSavedItem": False
            }
        ],
        "paKey": None,
        "customText": None
    }

    # Step 4: 요청 전송
    response = requests.post(
        url="https://beta-www.fashiongo.net/Cart/AddCart",
        headers=headers,
        data=json.dumps(payload)
    )

    # Step 5: 결과 확인
    if response.status_code == 200:
        print(f"🅿 [장바구니 성공] 상품ID={product_id}, 응답: {response.json()}")
        return True
    else:
        print(f"❌ [장바구니 실패] status: {response.status_code}, body: {response.text}")
        return False