from playwright.sync_api import Page, expect


# 페이지 함수 1: Order History 진입
def go_to_order_history(page: Page):
    print("☑ My Account 아바타 버튼 찾기")
    avatar_sel = 'a.user-avatar.nclick[data-nclick-name="site.menu.myaccount"]'
    page.wait_for_selector(avatar_sel)
    page.locator(avatar_sel).first.click()
    print("☑ 아바타 클릭 완료")

    order_history_sel = 'li.order-history.nclick[data-nclick-name="site.top.orderhistory"] a[href="/MyAccount/OrderHistory"]'
    page.wait_for_selector(order_history_sel)
    page.locator(order_history_sel).first.click()
    print("🅰 'Order History' 페이지 진입 완료")


# 페이지 함수 2: Newly Placed 주문 찾고 오더 디테일 진입
def open_newly_placed_order_detail(page: Page):
    print("☑ 주문 리스트 테이블 로딩 대기")
    page.wait_for_selector(".tab_ord table tbody tr")

    print("☑ 'Newly Placed'가 있는 행 찾기")
    # 7번째 컬럼(Order Status)에 'Newly Placed' 텍스트를 가진 tr 선택
    row_sel = ".tab_ord table tbody tr:has(td:nth-child(7):has-text('Newly Placed'))"
    rows = page.locator(row_sel)
    count = rows.count()
    print(f"☑ 후보 행 개수: {count}")

    if count == 0:
        # 상태 텍스트 자체가 있는지 추가 확인
        status_probe = page.locator(".tab_ord table tbody td:nth-child(7):has-text('Newly Placed')")
        print(f"❌ 상태 텍스트 존재 여부: {status_probe.count()}개")
        raise AssertionError("❌ 'Newly Placed' 상태의 주문 행을 찾지 못했습니다.")

    target_row = rows.first
    expect(target_row).to_be_visible
    print("🅿 대상 행 확인 완료")

    print("☑ 동일 행의 주문 상세 링크 클릭")
    # 예시 DOM: <a href="/MyAccount/OrderDetail/ALU4571427717" class="detail onsite-order">
    detail_link = target_row.locator("a.detail.onsite-order, a[href*='/MyAccount/OrderDetail/']").first
    expect(detail_link).to_be_visible
    detail_link.click()
    print("🅰 오더 디테일 페이지로 이동")

    page.wait_for_load_state("networkidle")


# 페이지 함수 3: 주문 취소 수행
def cancel_order(page: Page):
    print("☑ Cancel Order 버튼 클릭")
    page.wait_for_selector("button:has-text('Cancel Order')")
    page.click("button:has-text('Cancel Order')")
    print("☑ Confirm 모달 로딩 대기")

    # 모달 컨테이너와 헤더 텍스트(Confirm) 대기
    page.wait_for_selector(".middle-column .middle-column-header-text:has-text('Confirm')")
    page.wait_for_selector(".middle-column .middle-column-content-yes-no-buttons-container")

    print("☑ 모달의 Yes 버튼 클릭")
    yes_btn_sel = ".middle-column .middle-column-content-yes-no-buttons-container input[value='Yes']"
    expect(page.locator(yes_btn_sel).first).to_be_visible
    page.locator(yes_btn_sel).first.click()
    print("🅰 주문 취소 확정 클릭")

    print("☑ 'Canceled by Buyer' 상태 확인")
    expect(page.locator("text=Order Status: Canceled by Buyer")).to_be_visible(timeout=10000)
    print("🅿 주문 상태가 'Canceled by Buyer'로 변경됨")