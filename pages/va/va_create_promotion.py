from datetime import datetime, timedelta
from playwright.sync_api import Page

# Pages/front openpack order
async def va_create_promotion(page: Page):
    # 1. 메뉴 진입
    await page.locator("div.nav__item__title", has_text="Marketing Tools").click()
    await page.locator("a.nav__group__item__title", has_text="Vendor Promotion").click()
    await page.wait_for_url("**/marketing/special/promotion")

    # 2. 'Create Promotion' 클릭
    await page.locator("button.btn.btn-blue", has_text="Create Promotion").click()

    # 3. No end date 체크
    # await page.locator('.fg-checkbox.no-end-date label').click()

    # 4. 시작일 입력 (내일 날짜)
    tomorrow = (datetime.today() + timedelta(days=1)).strftime('%m/%d/%Y')
    await page.evaluate("""(date) => {
        const input = document.querySelector('input.datepicker.dateFrom');
        input.value = date;
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
    }""", tomorrow)

    # 4. 종료일 입력 (일주일 뒤 날짜)
    one_week_later = (datetime.today() + timedelta(days=7)).strftime('%m/%d/%Y')
    await page.evaluate("""(date) => {
        const input = document.querySelector('input.datepicker.dateTo');
        input.value = date;
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
    }""", one_week_later)

    # 5. 할인율 입력
    await page.fill('input#percent-input-3', '10')

    # 6. Save 클릭 (POST 발생 X)
    await page.locator('button.btn.btn-lg.btn-blue', has_text='Save Promotion').click()

    # 7. Confirm 클릭 직전: 응답 대기 세팅
    async with page.expect_response("**/api/discount/save/promotion") as save_response_info:
        await page.locator('button.btn.btn-md.btn-blue', has_text="Confirm").click()

    # 8. 응답 수신 및 discountId 추출
    save_response = await save_response_info.value
    assert save_response.status == 200, f"Promotion 저장 실패: {save_response.status}"

    save_data = await save_response.json()
    discount_id = save_data.get("data", {}).get("discountId")
    assert discount_id, "discountId 추출 실패"

    # 9. 고정된 Vendor ID 사용
    vendor_id = 16502

    print(f"[생성 완료] Discount ID: {discount_id}, Vendor ID: {vendor_id}")
    return discount_id, vendor_id