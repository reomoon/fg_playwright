import pytest
import aiohttp
from datetime import datetime
from core.page_wrapper import HighlightPageWrapper
from tests.va.test_va_login_fixture import va_login_fixture

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
        # ...상품 정보 생략 (기존 코드와 동일)...
        # (아래는 기존 코드 그대로 두시면 됩니다)
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

    # 비동기로 API 요청 보내고 응답 받기
    with aiohttp.ClientSession() as session:
        with session.post(url, headers=headers, json=payload) as response:
            resp_json = response.json()
            return response.status, resp_json

# 실제 테스트 함수
def test_create_item_api(login_fixture: HighlightPageWrapper):
    page = login_fixture

    # 1. localStorage에서 토큰 추출 (로그인 인증용)
    token = page.evaluate("() => localStorage.getItem('token')")

    # 2. localStorage에 없으면 쿠키에서 토큰 추출 시도
    if not token:
        cookies = page.context.cookies()
        for c in cookies:
            if c["name"] == "BETA_FG_TOKEN":
                token = c["value"]
                break

    # 3. 토큰이 없으면 테스트 실패
    assert token is not None, "BETA_FG_TOKEN not found in localStorage or cookies"
    print(f"[토큰 추출 완료] 앞 50자: {token[:50]}...")

    # 4. 상품 생성 API 호출 (비동기)
    status_code, json_data = call_item_save_api(token)

    # 5. 결과 확인 및 출력
    print(f"[응답 코드] {status_code}")
    print("[응답 결과]", json_data)

    # 6. 응답 코드와 성공 여부 검증
    assert status_code == 200, "응답 코드가 200이 아님"
    assert json_data.get("success", True), "API 응답 내 success=false"