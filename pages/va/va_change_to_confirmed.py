from playwright.sync_api import Page
import json


def open_first_new_order_detail(page: Page) -> None:
    """
    VA 사이드 메뉴에서
    1) Orders > All Orders > New Orders 로 진입하고
    2) New Orders 리스트의 첫 번째 주문을 클릭해서
    3) 주문 디테일 페이지로 이동하는 함수
    """

    # 1. 사이드 메뉴에서 'Orders' 메인 메뉴 찾기
    print("☑ 'Orders' 메인 메뉴 찾기")
    orders_main = page.locator("div.nav__item__title", has_text="Orders")
    print(f"☑ div.nav__item__title found ({page.locator('div.nav__item__title').count()}개)")
    orders_main.first.wait_for(state="visible", timeout=10000)
    print("🅿 'Orders' 메인 메뉴 표시 확인")

    # 1-1. 'Orders' 메인 메뉴 클릭 → 하위 메뉴 펼치기
    orders_main.first.click()
    print("☑ 'Orders' 메인 메뉴 클릭 (하위 메뉴 펼치기)")

    # 2. 'All Orders' 그룹 메뉴 찾기
    print("☑ 'All Orders' 하위 메뉴 찾기")
    all_orders_menu = page.locator("div.nav__group__item__title", has_text="All Orders")
    print(f"☑ div.nav__group__item__title found ({page.locator('div.nav__group__item__title').count()}개)")
    all_orders_menu.first.wait_for(state="visible", timeout=10000)
    print("🅿 'All Orders' 하위 메뉴 표시 확인")

    # 2-1. 'All Orders' 클릭 → New Orders 등 2차 메뉴 펼치기
    all_orders_menu.first.click()
    print("☑ 'All Orders' 메뉴 클릭 (2차 메뉴 펼치기)")

    # 3. 'New Orders' 2차 메뉴 클릭
    print("☑ 'New Orders' 2차 메뉴 찾기")
    new_orders_link = page.locator(
        "a.nav__sub-group2__item__title",
        has_text="New Orders"
    )
    print(f"☑ a.nav__sub-group2__item__title found ({page.locator('a.nav__sub-group2__item__title').count()}개)")
    new_orders_link.first.wait_for(state="visible", timeout=10000)
    print("🅿 'New Orders' 2차 메뉴 표시 확인")

    new_orders_link.first.click()
    print("☑ 'New Orders' 메뉴 클릭 (New Orders 리스트 페이지 이동)")

    # 3-1. 페이지 로드 대기 및 URL 검증
    page.wait_for_load_state("networkidle")
    current_url = page.url
    print(f"☑ 현재 URL: {current_url}")
    assert "/order/orders/new" in current_url, f"❌ New Orders 페이지가 아님: {current_url}"
    print("🅿 New Orders 리스트 페이지 진입 확인")

    # 4. New Orders 리스트에서 첫 번째 주문 행 찾기
    print("☑ New Orders 리스트의 행(selector: 'fg-order-list table tbody.ng-star-inserted tr') 로딩 대기")
    rows = page.locator("fg-order-list table tbody.ng-star-inserted tr")
    # New Orders 컴포넌트 안의 tbody tr 중 첫 번째가 보일 때까지 대기
    rows.first.wait_for(state="visible", timeout=10000)

    row_count = rows.count()
    print(f"☑ New Orders 리스트 행 개수: {row_count}개")
    assert row_count > 0, "❌ New Orders 리스트에 주문이 없습니다. (테스트용 주문 필요)"

    # 4-1. 첫 번째 행의 PO Number 링크 클릭 → 주문 디테일 페이지 이동
    # HTML 상에서 6번째 컬럼(td)에 PO Number 링크가 들어 있음
    print("☑ 첫 번째 주문 행의 PO Number 링크 찾기")
    first_po_link = rows.first.locator("td:nth-child(6) a[href^='#/order/']").first
    first_po_link.wait_for(state="visible", timeout=5000)
    print("🅿 PO Number 링크 표시 확인")

    first_po_link.click()
    print("☑ 첫 번째 주문의 PO Number 링크 클릭 (주문 디테일 페이지 이동)")

    print("☑ 주문 디테일 페이지 로딩 대기")
    page.wait_for_load_state("networkidle")

    # 5. URL이 디테일 페이지로 변경되었는지 확인
    detail_url = page.url
    print(f"☑ 이동 후 URL: {detail_url}")

    assert "/order/orders/new" not in detail_url, f"❌ 아직 New Orders 리스트에 머물러 있습니다: {detail_url}"
    assert "/order/" in detail_url, f"❌ 주문 디테일 페이지가 아닐 가능성이 있습니다: {detail_url}"
    print("🅿 New Orders 첫 번째 주문 디테일 페이지 진입 완료")


def change_order_status_to_confirmed(page: Page) -> None:
    """
    주문 디테일 페이지에서
    1) 상태 셀렉트 박스를 'Confirmed Orders'로 변경하고
    2) Update 버튼 클릭 시
    3) /api/order/.../save 요청의 body 에서 orderStatusId == 2 인지 검증
    """

    # 1. 상태 셀렉트 박스 찾기 (New Orders / Confirmed Orders 등 옵션 포함된 select)
    print("☑ 주문 상태 셀렉트 박스 찾기 (New Orders / Confirmed Orders 포함)")
    status_select = page.locator(
        "span.info-item__cont select"
    ).filter(has_text="New Orders").first

    status_select.wait_for(state="visible", timeout=10000)
    print("🅿 주문 상태 셀렉트 박스 표시 확인")

    # (선택) 현재 값이 New Orders인지 확인하고 싶으면 아래처럼 확인 가능
    try:
        current_value = status_select.input_value()
        print(f"☑ 현재 orderStatusId 값: {current_value}")
    except Exception:
        print("☑ 현재 값 읽기는 스킵 (중요하지 않으므로 무시)")

    # 2. 셀렉트 값을 'Confirmed Orders'(value=2) 로 변경
    print("☑ 주문 상태를 'Confirmed Orders'(value=2) 로 변경")
    status_select.select_option("2")
    print("🅿 주문 상태 select_option('2') 호출 완료")

    # 3. Update 버튼 찾기
    print("☑ 'Update' 버튼 찾기")
    update_button = page.locator("button.btn.btn-blue.btn--min-width", has_text="Update").first
    update_button.wait_for(state="visible", timeout=10000)
    print("🅿 'Update' 버튼 표시 확인")

    # 4. Update 클릭 시 /api/order/.../save 요청 캡쳐해서 orderStatusId 확인
    print("☑ 'Update' 클릭 시 /api/order/.../save 요청 대기 및 캡쳐")

    def _is_save_request(req):
        return (
            req.method == "POST"
            and "/api/order/" in req.url
            and req.url.endswith("/save")
        )

    with page.expect_request(_is_save_request) as req_info:
        update_button.click()
        print("☑ 'Update' 버튼 클릭 완료")

    save_request = req_info.value
    post_data = save_request.post_data or ""
    print(f"☑ save API 요청 URL: {save_request.url}")
    print(f"☑ save API 요청 body(raw): {post_data}")

    try:
        data = json.loads(post_data)
    except Exception as e:
        raise AssertionError(f"❌ save API body를 JSON으로 파싱하지 못했습니다: {e}, raw={post_data}")

    # 5. orderStatusId == 2 인지 검증
    order_status_id = data.get("orderStatusId")
    print(f"☑ save API body의 orderStatusId: {order_status_id}")

    assert order_status_id == 2, f"❌ orderStatusId가 2가 아님: {order_status_id}"
    print("🅿 orderStatusId가 2(Confirmed) 로 저장된 것 확인")