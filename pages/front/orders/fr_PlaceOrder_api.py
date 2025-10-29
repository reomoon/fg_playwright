import json
import time
import requests


def get_cookie_header(page):
    """
    Playwright 페이지 객체에서 쿠키를 추출하여
    requests 요청에 사용할 수 있는 Cookie 헤더 형식으로 반환
    """
    cookies = page.context.cookies()
    return "; ".join([f"{c['name']}={c['value']}" for c in cookies])


def get_credit_card_and_buyer_id(page, referer=None):
    """
    신용카드 리스트 API를 호출해 첫 번째 카드의
    creditCardId와 buyerId(retailerId)를 반환
    """
    ts = int(time.time() * 1000)
    url = f"https://beta-www.fashiongo.net/MyAccount/CreditCard/GetCreditCardListSimple?_={ts}"

    headers = {
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0",
        "Cookie": get_cookie_header(page),
    }
    if referer:
        headers["Referer"] = referer

    try:
        resp = requests.get(url, headers=headers)
        data = resp.json().get("data", {})
    except Exception as e:
        print(f"[에러] 카드 리스트 조회 실패: {e}")
        return None, None

    # 응답 형태: {"data": {"ccList": [...]}} 또는 {"data": [...]}
    cc_list = data.get("ccList") if isinstance(data, dict) else data
    if not isinstance(cc_list, list) or not cc_list:
        print("[에러] 카드 리스트 없음")
        return None, None

    card = cc_list[0]
    return card.get("creditCardId"), card.get("retailerId")


def get_default_shipping_address_id(page):
    """
    배송지 목록 API를 호출하여 isDefault가 true인
    배송지의 saId 또는 said 값을 반환
    """
    ts = int(time.time() * 1000)
    url = f"https://beta-www.fashiongo.net/MyAccount/ShipAddress/json/Get?act=1&_={ts}"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://beta-www.fashiongo.net/MyAccount/ShipAddress",
        "Cookie": get_cookie_header(page),
    }

    try:
        resp = requests.get(url, headers=headers)
        json_data = resp.json()
        print("[DEBUG] 배송지 응답 본문:", json_data)
        # 정확한 경로로 shipAddrList 접근
        data = json_data.get("data", {}).get("shipAddrList", [])
    except Exception as e:
        print(f"[에러] 배송지 조회 실패: {e}")
        return None

    if not isinstance(data, list):
        print("[경고] 배송지 응답이 리스트 형태가 아님")
        return None

    for addr in data:
        if isinstance(addr, dict) and (addr.get("isDefault") or addr.get("isdefault")):
            return str(addr.get("saId") or addr.get("said"))

    print("[경고] 기본 배송지를 찾지 못함")
    return None


def place_order(page, session_id, vendor_id="16502", ship_method_id=3):
    """
    PlaceOrder API 호출
    순서:
      1. 카드 ID, 구매자 ID 조회
      2. 기본 배송지 ID 조회
      3. 주문 생성 API 호출
    """
    referer = f"https://beta-www.fashiongo.net/Checkout/{session_id}?premiumCouponIssueId=0&allCouponIssueId=0"
    cookie = get_cookie_header(page)

    # 1. 카드 정보 조회
    cc_id, buyer_id = get_credit_card_and_buyer_id(page, referer)
    if not cc_id or not buyer_id:
        print("[에러] 카드 또는 구매자 ID 조회 실패")
        return False

    # 2. 배송지 정보 조회
    sa_id = get_default_shipping_address_id(page)
    if not sa_id:
        print("[에러] 기본 배송지 ID 조회 실패")
        return False

    # 3. 주문 요청
    url = f"https://beta-www.fashiongo.net/Checkout/PlaceOrder/{session_id}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": "https://beta-www.fashiongo.net",
        "Referer": referer,
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0",
        "Cookie": cookie,
    }

    payload = {
        "buyerId": str(buyer_id),
        "sessionId": session_id,
        "couponIssueId": "",
        "shippingAddressId": sa_id,
        "paymentMethodId": 6,  # 6: 신용카드
        "paymentMethod": "Credit Card",
        "creditCardId": cc_id,
        "linesheetId": None,
        "vendorSpecific": {
            str(vendor_id): {
                "shipMethodId": ship_method_id,
                "buyerShippingAccount": None,
                "comments": None,
                "shipAll": False,
                "customTruckingName": None,
                "buyerPONumber": "",
                "insurance": False,
                "signature": False,
                "labelingService": False,
                "appliedCouponIssueId": None,
                "orderHash": "",
            }
        },
    }

    try:
        resp = requests.post(url, headers=headers, data=json.dumps(payload))
        result = resp.json()
    except Exception as e:
        print(f"[에러] 주문 응답 파싱 실패: {e}")
        print("본문:", resp.text[:300])
        return False

    if result.get("success"):
        print("[성공] 주문 완료:", result)
        return True

    print("[실패] 주문 실패:", result)
    return False