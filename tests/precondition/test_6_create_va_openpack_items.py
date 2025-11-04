import requests
from datetime import datetime
from core.page_wrapper import HighlightPageWrapper
from tests.va.test_va_login_fixture import va_login_fixture

# ✅ [공유 헬퍼] 응답 JSON에서 productId 안전 추출
def _extract_product_id(data):
    if isinstance(data, dict) and isinstance(data.get("data"), int):
        return data["data"]
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

# ✅ productId 파일 저장
def _save_product_id(product_id, filepath="openpack_productid.txt"):
    try:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(f"{product_id}\n")
        print(f"🅿 [상품ID 저장 성공] {product_id} → {filepath}")
    except Exception as e:
        print("❌ [상품ID 저장 실패]", e)

# ✅ 오픈팩 상품 생성 API 호출
def call_item_save_api_openpack(token):
    url = "https://beta-vendoradmin.fashiongo.net/api/item/save"

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item_name = f"test openpack {now_str}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://beta-vendoradmin.fashiongo.net",
        "Referer": "https://beta-vendoradmin.fashiongo.net/",
        "User-Agent": "Mozilla/5.0"
    }

    # ⚠️ 필요한 값(카테고리/사이즈차트/컬러/이미지)은 환경에 맞게 유지
    # - sizeId: 사이즈 차트(예: S/M/L가 있는 차트 ID). 기존과 동일 값 사용.
    # - colorId: 실제 활성 컬러 ID 사용.
    # - imageUrl: 접근 가능한 벤더 이미지 경로 사용.
    payload = {
        "item": {
            "active": True,
            "productName": "openpackstyleno",
            "sellingPrice": 22,
            "sizeId": 48551,  # S/M/L를 포함한 사이즈 차트
            "description": "openpack description",
            "activatedOn": now_str,
            "itemName": item_name,
            "parentParentCategoryId": 1,
            "parentCategoryId": 501,
            "categoryId": 32,
            "fashionGoExclusive": False,
            "labelTypeId": 1,
            "prePackYN": "N",  # ✅ 오픈팩
            "weightUnit": "lb",
            "isReturnable": True,
            "evenColorYN": False,
            "colorCount": 1,
            "fgFreeShippingDisabled": False,
            "inActive": "openpackstyleno"
        },
        # (선택) 구버전 inventory는 최소한만 유지 (실제 재고는 inventoryOpenpack에서 반영)
        "inventory": {
            "update": [
                {"active": True, "available": True, "sizeName": "S", "colorId": 893825},
                {"active": True, "available": True, "sizeName": "M", "colorId": 893825},
                {"active": True, "available": True, "sizeName": "L", "colorId": 893825}
            ],
            "delete": []
        },
        "image": {
            "update": [{
                "active": True,
                "imageName": "16502-1756101330184-2025-03-18 15 35 14.jpg",
                "imageUrl": "https://beta-volatile-download.fashiongo.net/vendor-upload/item/16502/16502-1756101330184-2025-03-18 15 35 14.jpg",
                "listOrder": 1,
                "productId": 0,
                "download": "https://beta-volatile-download.fashiongo.net/vendor-upload/item/16502/16502-1756101330184-2025-03-18 15 35 14.jpg",
                "loaded": True
            }],
            "delete": []
        },
        "changedInfo": {
            "newPictureGeneral": "16502-1756101330184-2025-03-18 15 35 14.jpg",
            "packId": 0,     # ✅ 오픈팩은 packId 없음
            "active": True
        },
        "inventoryV2": {
            "saved": [{
                "inventoryOpenpack": [{
                    "colorId": 893825,
                    "colorName": "RED",
                    "qty": [
                        {
                            "active": True,
                            "availableOn": None,
                            "inventoryId": None,
                            "sizeName": "S",
                            "qtyUpdated": False,
                            "colorId": 893825,
                            "colorName": "RED",
                            "productId": None,
                            "qty": 999,
                            "status": "In Stock",
                            "statusCode": 1,
                            "threshold": 0,
                            "invUpdated": True
                        },
                        {
                            "active": True,
                            "availableOn": None,
                            "inventoryId": None,
                            "sizeName": "M",
                            "qtyUpdated": False,
                            "colorId": 893825,
                            "colorName": "RED",
                            "productId": None,
                            "qty": 999,
                            "status": "In Stock",
                            "statusCode": 1,
                            "threshold": 0,
                            "invUpdated": True
                        },
                        {
                            "active": True,
                            "availableOn": None,
                            "inventoryId": None,
                            "sizeName": "L",
                            "qtyUpdated": False,
                            "colorId": 893825,
                            "colorName": "RED",
                            "productId": None,
                            "qty": 999,
                            "status": "In Stock",
                            "statusCode": 1,
                            "threshold": 0,
                            "invUpdated": True
                        }
                    ]
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

# ✅ 실제 테스트
def test_create_openpack_item_api(va_login_fixture: HighlightPageWrapper):
    page = va_login_fixture

    # 1) localStorage → 2) cookie 순으로 토큰 조회 (prepack과 동일)
    token = page.evaluate("() => localStorage.getItem('token')")
    if not token:
        cookies = page.context.cookies()
        for c in cookies:
            if c.get("name") == "BETA_FG_TOKEN":
                token = c.get("value")
                break

    assert token is not None, "BETA_FG_TOKEN not found in localStorage or cookies"
    print(f"☑ [토큰 추출 완료] 앞 50자: {token[:50]}...")

    # 2) API 호출
    response = call_item_save_api_openpack(token)

    # 3) 응답 검사 + productId 저장 (prepack과 동일)
    print(f"☑ [응답 코드] {response.status_code}")
    try:
        json_data = response.json()
        print("☑ [응답 결과]", json_data)

        assert response.status_code == 200, "응답 코드가 200이 아님"
        assert json_data.get("success", True), "API 응답 내 success=false"

        product_id = _extract_product_id(json_data)
        if product_id is not None:
            _save_product_id(product_id, "openpack_productid.txt")
        else:
            print("❌ [상품ID 추출 실패] 응답 내 data/productId 없음")

    except Exception as e:
        print("❌ [응답 파싱 실패]", e)
        print(response.text)
        assert False, "응답을 JSON으로 파싱하지 못함"