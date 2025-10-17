from playwright.sync_api import Page
from pages.front.items.fr_AddtoCart import add_item_to_cart
from tests.front.login.test_front_login_fixture import front_login_fixture

def test_items(front_login_fixture):
    page = front_login_fixture  # 로그인된 페이지 사용

    # 1) Best of Best 페이지로 이동
    page.goto("https://beta-www.fashiongo.net/Best")
    page.wait_for_load_state("networkidle")

    # 2) 첫 번째 상품 타일 클릭 (안정적인 셀렉터 사용)
    image_link = page.locator(
        'ul.lst_pdt li div.pic a.nclick[href^="/Item/"]:has(img[name="productImage"])'
    ).first

    image_link.wait_for(state="visible", timeout=15000)
    # 클릭 시 상세 페이지로 이동 완료될 때까지 기다림
    with page.expect_navigation():
        image_link.click()

    # 3) 상세 페이지 로딩 완료 대기 (SPA 전환 방지)
    page.wait_for_url("**/Item/**", timeout=15000)
    page.wait_for_load_state("networkidle")

    # 4) 장바구니 담기 함수 실행 (내부에서 입력칸 대기 포함)
    add_item_to_cart(page)

    # 5) 현재 상세페이지의 URL에서 상품 ID 추출
    product_id = page.url.split('/')[-1].split('?')[0]
    print("추출한 Product ID:", product_id)

    # 6) 장바구니 페이지로 이동
    page.goto("https://beta-www.fashiongo.net/cart")
    page.wait_for_load_state("networkidle")

    # 7) 장바구니 내 해당 상품이 존재하는지 확인
    selector = f".goods-detail[id='{product_id}']"
    item_in_cart = page.locator(selector)

    # 8) 검증: 상품이 장바구니에 존재해야 함
    assert item_in_cart.count() > 0, f"장바구니에 Product ID {product_id}가 존재하지 않음"