from datetime import datetime, timedelta
from playwright.sync_api import Page
import pytest

#프로모션 생성 시 할인율
promotion_discount = 7

# Pages/front openpack order
def va_create_promotion(page: Page):
    # 1. 메뉴 진입
    # page.locator("div.nav__item__title", has_text="Marketing Tools").click()
    # page.locator("a.nav__group__item__title", has_text="Promotions").click()
    # page.locator("a.nav__sub-group2__item__title", has_text="Vendor Promotion").click()
    page.goto("https://beta-vendoradmin.fashiongo.net/#/marketing/special/promotion/vendor", timeout=10000, wait_until="domcontentloaded")
    # page.wait_for_url("**/marketing/special/promotion/vendor")

    # 2. 여러 개 중 enabled인 버튼만 클릭
    create_btns = page.locator("button.btn.btn-md.btn-blue", has_text="Create Promotion")

    btn_count = create_btns.count()
    print(f"☑ button.btn.btn-md.btn-blue found ({btn_count}개)")

    if btn_count == 0:
        pytest.skip("'Create Promotion' 버튼이 아예 없어 테스트를 스킵합니다.")
        return

    # 비활성화 버튼들을 제외한 enabled 버튼 필터링
    enabled_btn = page.locator(
        "button.btn.btn-md.btn-blue:not(.btn-grey):not([disabled])",
        has_text="Create Promotion"
    )

    enabled_count = enabled_btn.count()
    print(f"☑ enabled Create Promotion 버튼 개수: {enabled_count}개")

    # 비활성화만 존재하면 스킵 처리
    if enabled_count == 0:
        print("🗙 Create Promotion 버튼이 disabled 상태입니다. 테스트를 스킵합니다.")
        pytest.skip("Create Promotion 버튼이 disabled 상태라 테스트를 진행할 수 없습니다.")
        return

    # Spinner가 사라질 때까지 기다림 (로딩 완료)
    page.wait_for_selector("div.spinner", state="hidden", timeout=30000)
    print("☑ 로딩 완료 (spinner 사라짐)")
    page.wait_for_timeout(1000)  # 추가 안정화 대기
    
    create_btns.first.click(force=True, timeout=30000)

    # 3. No end date 체크
    # page.locator('.fg-checkbox.no-end-date label').click()

    # 4. 시작일 입력 (내일 날짜)
    tomorrow = (datetime.today() + timedelta(days=1)).strftime('%m/%d/%Y')
    page.evaluate("""(date) => {
        const input = document.querySelector('input.datepicker.dateFrom');
        input.value = date;
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
    }""", tomorrow)

    # 4. 종료일 입력 (일주일 뒤 날짜)
    one_week_later = (datetime.today() + timedelta(days=7)).strftime('%m/%d/%Y')
    page.evaluate("""(date) => {
        const input = document.querySelector('input.datepicker.dateTo');
        input.value = date;
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
    }""", one_week_later)

    # 5. 할인율 입력
    # 요소가 visible할 때까지 기다림
    page.locator('input#percent-input-3').wait_for(state="visible", timeout=30000)
    page.wait_for_timeout(1000)  # 안정화 대기

    # fill 대신 evaluate로 직접 입력 (더 안정적)
    page.evaluate("""(value) => {
        const input = document.querySelector('input#percent-input-3');
        input.value = value;
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
    }""", str(promotion_discount))

    print(f"☑ 할인율 {promotion_discount}% 입력 완료")

    # 6. Save 클릭 (POST 발생 X)
    page.locator('button.btn.btn-lg.btn-blue', has_text='Save Promotion').click()

    # 7. Confirm 클릭 직전: 응답 대기 세팅
    with page.expect_response("**/api/discount/save/promotion") as save_response_info:
        page.locator('button.btn.btn-md.btn-blue', has_text="Confirm").click()

    # 8. 응답 수신 및 discountId 추출
    save_response = save_response_info.value
    assert save_response.status == 200, f"Promotion 저장 실패: {save_response.status}"

    save_data = save_response.json()
    discount_id = save_data.get("data", {}).get("discountId")
    assert discount_id, "discountId 추출 실패"

    # 9. 고정된 Vendor ID 사용
    vendor_id = 16502

    print(f"[생성 완료] Discount ID: {discount_id}, Vendor ID: {vendor_id}")
    return discount_id, vendor_id