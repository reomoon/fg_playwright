import json
import requests

def get_cookie_header_from_page(page):
    cookies = page.context.cookies()
    return "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

def add_item_to_cart(page):
    cookie_header = get_cookie_header_from_page(page)

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/json; charset=UTF-8",
        "Origin": "https://beta-www.fashiongo.net",
        "Referer": "https://beta-www.fashiongo.net/Item/24266430?paKey=20250804c1680d1e58a65570597ab09f7266ad6c",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0",
        "Cookie": cookie_header,
    }

    payload = {
        # 3064 = 1 funky
        # 16502 = allium
        "wholeSalerId": "3064",
        "retailerId": "566735",
        "productId": "24266430",
        "sizeId": "25738",
        "colorPacks": [
            {
                "id": "0",
                "colorId": "1292925",
                "colorName": "ASH TAUPE",
                "qty": ["9", "6", "3", "0", "0", "0", "0", "0", "0", "0", "18"],
                "pkQty": "3",
                "unitPrice": "12",
                "isSavedItem": False
            }
        ],
        "paKey": "20250804c1680d1e58a65570597ab09f7266ad6c",
        "customText": None
    }

    response = requests.post(
        url="https://beta-www.fashiongo.net/Cart/AddCart",
        headers=headers,
        data=json.dumps(payload)
    )

    if response.status_code == 200:
        print("[✅ AddCart 성공] 응답:", response.json())
        return True
    else:
        print(f"[❌ AddCart 실패] status: {response.status_code}, body: {response.text}")
        return False