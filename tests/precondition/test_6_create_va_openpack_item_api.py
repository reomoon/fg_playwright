import requests
from datetime import datetime
from core.page_wrapper import HighlightPageWrapper
from tests.va.test_va_login_fixture import va_login_fixture

# 상품 생성 API 호출 함수 (비동기)
def call_item_save_api_openpack(token):
    url = "https://vendoradmin.fashiongo.net/api/item/save"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item_name = f"test openpack {now_str}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://vendoradmin.fashiongo.net",
        "Referer": "https://vendoradmin.fashiongo.net/",
        "User-Agent": "Mozilla/5.0"
    }

    payload = {
        "item": {
            "active": True,
            "productName": "openpackstyleno",
            "sellingPrice": 22,
            "sizeId": 48551,
            "description": "openpack description",
            "activatedOn": now_str,
            "itemName": item_name,
            "parentParentCategoryId": 1,
            "parentCategoryId": 501,
            "categoryId": 32,
            "fashionGoExclusive": False,
            "labelTypeId": 1,
            "prePackYN": "N",  # ✅ 오픈팩 설정
            "weightUnit": "lb",
            "isReturnable": True,
            "evenColorYN": False,
            "colorCount": 1,
            "fgFreeShippingDisabled": False,
            "inActive": "openpackstyleno"
        },
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
                "imageUrl": "https://volatile-download.fashiongo.net/vendor-upload/item/16502/16502-1756101330184-2025-03-18 15 35 14.jpg",
                "listOrder": 1,
                "productId": 0,
                "download": "https://volatile-download.fashiongo.net/vendor-upload/item/16502/16502-1756101330184-2025-03-18 15 35 14.jpg",
                "loaded": True
            }],
            "delete": []
        },
        "changedInfo": {
            "newPictureGeneral": "16502-1756101330184-2025-03-18 15 35 14.jpg",
            "packId": 0,
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
        
# 실제 테스트 함수
def test_create_openpack_item_api(va_login_fixture: HighlightPageWrapper):
    page = va_login_fixture
    token = page.evaluate("() => localStorage.getItem('token')")
    if not token:
        cookies = page.context.cookies()
        for c in cookies:
            if c["name"] == "BETA_FG_TOKEN":
                token = c["value"]
                break
    assert token is not None, "BETA_FG_TOKEN not found"
    print(f"☑ [토큰 추출 완료] 앞 50자: {token[:50]}...")

    response = call_item_save_api_openpack(token)

    print(f"☑ [응답 코드] {response.status_code}")
    try:
        json_data = response.json()
        print("☑ [응답 결과]", json_data)
        assert response.status_code == 200
        assert json_data.get("success", True)
    except Exception as e:
        print("❌ [응답 파싱 실패]", e)
        print(response.text)
        assert False, "응답을 JSON으로 파싱하지 못함"