import pytest
from tests.web.FR_tests.test_login import login_fixture
from playwright.sync_api import Page
from Pages.web.FR_Pages.Items.Addtocart import add_item_to_cart

def test_FR_9_items(login_fixture):
    page = login_fixture  # 로그인된 페이지 사용

    # 1. Best of Best 페이지 이동
    page.goto("https://beta-www.fashiongo.net/Best")

    # 2. 첫 번째 아이템 클릭
    image_link = page.locator('ul.lst_pdt li .pic a.nclick').first
    image_link.scroll_into_view_if_needed()
    image_link.wait_for(state='visible', timeout=5000)
    image_link.click()

    # 3. 아이템 상세 페이지 로딩 대기
    page.wait_for_load_state('load')
    page.wait_for_selector("input.txtPkQty, input.jsOpenPackEachQty", timeout=10000)

    # 4. 장바구니에 아이템 추가
    add_item_to_cart(page)

    # 5. Product ID 추출 (상세페이지에서)
    product_id = page.url.split('/')[-1].split('?')[0]
    print("추출한 Product ID:", product_id)

    # 6. 장바구니 페이지로 이동
    page.goto("https://beta-www.fashiongo.net/cart")
    page.wait_for_load_state('load')

    # 7. 장바구니에 해당 상품이 있는지 확인
    selector = f".goods-detail[id='{product_id}']"
    item_in_cart = page.locator(selector)

    # 8. 검증
    assert item_in_cart.count() > 0, f"장바구니에 Product ID {product_id}가 존재하지 않음"

    print(f"장바구니에 Product ID {product_id}가 정상적으로 존재함")