import requests
from datetime import datetime
from core.page_wrapper import HighlightPageWrapper
from tests.va.test_va_login_fixture import va_login_fixture

# ✅ [추가] 응답 JSON에서 productId를 안전하게 찾아주는 작은 헬퍼
def _extract_product_id(data):
    # 1) 응답이 {"success": True, "data": 24719749, ...} 형태라면 바로 반환
    if isinstance(data, dict) and isinstance(data.get("data"), int):
        return data["data"]

    # 2) fallback: productId / product_id / id 전역 탐색 (기존 로직 유지)
    targets = ("productId", "product_id", "id")
    found = []

    def _walk(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in targets:
                    if isinstance(v, int):
                        found.append(v)
                    elif isinstance(v, str) and v.isdigit():
                        found.append(int(v))
                _walk(v)
        elif isinstance(obj, list):
            for e in obj:
                _walk(e)

    _walk(data)
    return found[0] if found else None

# ✅ [추가] productId를 productid.txt에 저장 (파일 없으면 자동 생성)
def _save_product_id(product_id, filepath="prepack_productid.txt"):
    try:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(f"{product_id}\n")
        print(f"🅿 [상품ID 저장 성공] {product_id} → {filepath}")
    except Exception as e:
        print("❌ [상품ID 저장 실패]", e)

# 상품 생성 API를 호출하는 비동기 함수
def call_item_save_api(token):
    url = "https://beta-vendoradmin.fashiongo.net/api/item/save"

    # 현재 시간을 이용해 상품 이름 생성
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item_name = f"test prepack {now_str}"

    # API 요청에 필요한 헤더 설정 (인증 토큰 등)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://beta-vendoradmin.fashiongo.net",
        "Referer": "https://beta-vendoradmin.fashiongo.net/",
        "User-Agent": "Mozilla/5.0"
    }

    # 실제로 저장할 상품 정보(딕셔너리)
    payload = {
        "item": {
            "active": True,
            "productName": "prepackstyleno",
            "sellingPrice": 22,
            "sizeId": 48551,
            "description": "prepackdescription",
            "activatedOn": now_str,
            "itemName": item_name,
            "parentParentCategoryId": 1,
            "parentCategoryId": 501,
            "categoryId": 32,
            "fashionGoExclusive": False,
            "packId": 47941,
            "labelTypeId": 1,
            "prePackYN": "Y",
            "weightUnit": "lb",
            "isReturnable": True,
            "evenColorYN": False,
            "colorCount": 1,
            "fgFreeShippingDisabled": False,
            "inActive": "teststyleno"
        },
        "inventory": {
            "update": [{
                "active": True,
                "available": True,
                "colorId": 893825
            }],
            "delete": []
        },
        "image": {
            "update": [{
                "active": True,
                "imageName": "16502-1755754176380-2025-03-18 15 35 14.jpg",
                "imageUrl": "https://fg-image.fashiongo.net/Vendors/yz9w6rpkaz/ProductImage/large/C062A9FD81134CA676182D2C1D4BB0A7/14925243_24f990dc-eb77-4f0b-9196-fc940a28482e.jpg",
                "listOrder": 1,
                "productId": 0,
                "download": "https://fg-image.fashiongo.net/Vendors/yz9w6rpkaz/ProductImage/large/C062A9FD81134CA676182D2C1D4BB0A7/14925243_24f990dc-eb77-4f0b-9196-fc940a28482e.jpg",
                "loaded": True
            }],
            "delete": []
        },
        "changedInfo": {
            "newPictureGeneral": "16502-1755754176380-2025-03-18 15 35 14.jpg",
            "packId": 47941,
            "active": True
        },
        "inventoryV2": {
            "saved": [{
                "productId": None,
                "inventoryPrepack": [{
                    "active": True,
                    "colorId": 893825,
                    "colorName": "RED",
                    "qty": 999,
                    "status": "In Stock",
                    "statusCode": 1,
                    "threshold": 0,
                    "invUpdated": True,
                    "qtyUpdated": False
                }]
            }],
            "deleted": []
        },
        "customization": {
            "isActive": False
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return response

# 실제 테스트 함수
def test_create_item_api(va_login_fixture: HighlightPageWrapper):
    page = va_login_fixture

    # Step 1: localStorage에서 토큰 추출
    token = page.evaluate("() => localStorage.getItem('token')")

    # Step 2: 없으면 cookie에서 추출 시도
    if not token:
        cookies = page.context.cookies()
        for c in cookies:
            if c["name"] == "BETA_FG_TOKEN":
                token = c["value"]
                break

    # Step 3: 최종 확인
    assert token is not None, "BETA_FG_TOKEN not found in localStorage or cookies"
    print(f"☑ [토큰 추출 완료] 앞 50자: {token[:50]}...")

    # Step 4: 상품 생성 API 호출
    response = call_item_save_api(token)

    # Step 5: 결과 확인 및 저장
    print(f"☑ [응답 코드] {response.status_code}")
    try:
        json_data = response.json()
        print("☑ [응답 결과]", json_data)

        assert response.status_code == 200, "응답 코드가 200이 아님"
        assert json_data.get("success", True), "API 응답 내 success=false"

        # productId = json_data["data"] 우선 확인 → 없으면 fallback
        product_id = _extract_product_id(json_data)
        if product_id is not None:
            _save_product_id(product_id, "prepack_productid.txt")
        else:
            print("❌ [상품ID 추출 실패] 응답 내 data/productId 없음")

    except Exception as e:
        print("❌ [응답 파싱 실패]", e)
        print(response.text)
        assert False, "응답을 JSON으로 파싱하지 못함"