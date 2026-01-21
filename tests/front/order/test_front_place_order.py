from playwright.sync_api import Page
from tests.front.login.test_front_login_fixture import front_login_fixture
from pages.front.orders.fr_Checkout import checkout_flow
from pages.front.items.fr_AddtoCart import run_add_to_cart_flow


def test_place_order(front_login_fixture: Page):
    """
    전체 플로우:
    1) 로그인된 페이지(front_login_fixture)로 진입
    2) API로 장바구니에 아이템 담기
    3) checkout_flow()로 체크아웃 + 오더 검증
    """
    page = front_login_fixture

    print("🅰 Front 계정 로그인 완료 - 장바구니 담기 시작")

    # 1. 장바구니에 아이템 담기 (API 기반)
    run_add_to_cart_flow(page)
    print("🅿 장바구니 담기 완료 - 체크아웃 플로우 시작")

    # 2. 체크아웃 플로우 실행
    success, message = checkout_flow(page)

    # 3. 실패 시, message에 어떤 단계에서 무엇 때문에 실패했는지 그대로 출력
    assert success, message