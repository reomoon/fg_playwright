import re # 모듈을 사용하면 문자열에서 특정 패턴을 찾거나 치환하거나 분리할 수 있음

# Lib/mobile_utils.py

async def MO_checkout(page):
    '''
    모바일 checkout 함수, Cart 부터 시작 (비동기)
    '''
    # Checkout All Vendor 버튼 클릭 후 split-orders 페이지로 이동
    async with page.expect_navigation(url="**/checkout/split-orders?cartId=**", timeout=20000) as nav_info:
        await page.locator('button.checkout-btn.nclick').click()

    # 반드시 with 블록이 끝난 후에 URL을 가져와야 함!
    split_url = (await nav_info.value).url if nav_info.value else page.url
    print(f"split_url 원본: {split_url}")

    # URL에서 &fsv= 이하의 쿼리 파라미터는 제거 (cartId 추출에 불필요한 부분 제거)
    if '&fsv=' in split_url:
        split_url = split_url.split('&fsv=')[0]
    print(f"split_url: {split_url}")

    # 정규 표현식으로 split_url에서 cartId 값을 추출
    match = re.search(r'cartId=([a-z0-9\-]+)', split_url)
    cart_id = match.group(1) if match else None
    print(f"cartId: {cart_id}")

    # You Have Promotions! 팝업 있으면 클릭 없으면 스킵
    try:
        popup_promotion = page.locator_popup('button.btn-sure', has_text="Continue To Checkout")
        if await popup_promotion.is_visible() and await popup_promotion.count() > 0 and await popup_promotion.is_enabled():
            await popup_promotion.click()
            print("You Have Promotions! 팝업이 표시되었습니다.")
        else:
            print("You Have Promotions! 팝업이 표시되지 않았습니다.")
    except Exception as e:
        print(f"팝업 처리 중 예외발생, 스킵하고 진행합니다:{e}")

    await page.wait_for_timeout(2000)  # 2초 대기

    """
    🟢 Step1 Shipping
    """
    # Save & Continue
    await page.locator('button.base-btn.primary.medium.ng-star-inserted').click()
    await page.wait_for_timeout(2000)  # 2초 대기

    # Verify Your Address 팝업 있으면 클릭 없으면 스킵
    try:
        popup_verify = page.locator_popup('button.btn-black.btn-btm-main', has_text="Keep This Address")
        if await popup_verify.is_visible() and await popup_verify.count() > 0 and await popup_verify.is_enabled():
            await popup_verify.click()
            print("Verify Your Address 팝업이 표시되었습니다.")
        else:
            print("Verify Your Address 팝업이 표시되지 않았습니다.")
    except Exception as e:
        print(f"팝업 처리 중 예외발생, 스킵하고 진행합니다:{e}")

    """
    🟢 Step2 Payment
    """
    # Save & Continue
    await page.locator('button.base-btn.primary.medium.ng-star-inserted').click()
    await page.wait_for_timeout(2000)  # 2초 대기

    # 백업카드 팝업이 있으면 x버튼 클릭 없으면 스킵
    try:
        popup_backupcard = page.locator('div.modal__content__header__close')
        if await popup_backupcard.is_visible() and await popup_backupcard.count() > 0 and await popup_backupcard.is_enabled():
            await popup_backupcard.click()
            print("Backup Card 팝업이 표시되었습니다.")
        else:
            print("Backup Card 팝업이 표시되지 않았습니다.")
    except Exception as e:
        print(f"팝업 처리 중 예외발생, 스킵하고 진행합니다:{e}")

    # 백업카드 팝업이 있으면 x버튼 클릭 없으면 스킵(다시 팝업 나오는 경우)
    try:
        popup_backupcard = page.locator('div.modal__content__header__close')
        if await popup_backupcard.is_visible() and await popup_backupcard.count() > 0 and await popup_backupcard.is_enabled():
            await popup_backupcard.click()
            print("Backup Card 팝업이 표시되었습니다.")
        else:
            print("Backup Card 팝업이 표시되지 않았습니다.")
            await page.locator('button.base-btn.primary.medium.ng-star-inserted').click()
    except Exception as e:
        print(f"팝업 처리 중 예외발생, 스킵하고 진행합니다:{e}")

    """
    🟢 Step3_Order Review
    """
    # Submit Order
    submit_btn = page.locator('button.base-btn.primary.medium.ng-star-inserted', has_text="Submit Order")
    if await submit_btn.is_visible() and await submit_btn.is_enabled():
        await submit_btn.click()
        print("Submit Order 버튼 클릭됨")
    else:
        print("Submit Order 버튼이 비활성화 또는 숨겨져 있음")
    await page.wait_for_url("**/checkout/confirm/**", timeout=10000)  # 주문 완료 페이지로 이동할 때까지 대기

    order_confirm_url = page.url
    print(f"order confirm URL: {order_confirm_url}")

    # 주문 성공 여부 판정
    expected_url = f"https://beta-mobile.fashiongo.net/checkout/confirm/{cart_id}"
    if order_confirm_url.startswith(expected_url):
        print(f"Card Id: '{cart_id}' 주문 성공")
    else:
        print("주문 실패")

    await page.wait_for_timeout(2000)  # 네트워크/페이지 이동 대기