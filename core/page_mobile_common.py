import re # 모듈을 사용하면 문자열에서 특정 패턴을 찾거나 치환하거나 분리할 수 있음

# Lib/mobile_utils.py

def MO_checkout(page):
    '''
    모바일 checkout 함수, Cart 부터 시작 (비동기)
    '''
    # Checkout All Vendor 버튼 클릭 후 split-orders 페이지로 이동
    with page.expect_navigation(url="**/checkout/split-orders?cartId=**", timeout=20000) as nav_info:
        page.locator('button.checkout-btn.nclick').click()

    # 반드시 with 블록이 끝난 후에 URL을 가져와야 함!
    split_url = (nav_info.value).url if nav_info.value else page.url
    print(f"☑ split_url 원본: {split_url}")

    # URL에서 &fsv= 이하의 쿼리 파라미터는 제거 (cartId 추출에 불필요한 부분 제거)
    if '&fsv=' in split_url:
        split_url = split_url.split('&fsv=')[0]
    print(f"☑ split_url: {split_url}")

    # 정규 표현식으로 split_url에서 cartId 값을 추출
    match = re.search(r'cartId=([a-z0-9\-]+)', split_url)
    cart_id = match.group(1) if match else None
    print(f"☑ cartId: {cart_id}")

    # You Have Promotions! 팝업 있으면 클릭 없으면 스킵
    try:
        popup_promotion = page.locator('button.btn-sure', has_text="Continue To Checkout", log_if_not_found=False)
        if popup_promotion.is_visible() and popup_promotion.count() > 0 and popup_promotion.is_enabled():
            popup_promotion.click()
            print("☑ You Have Promotions! 팝업이 표시되었습니다.")
        else:
            print("☑ You Have Promotions! 팝업이 표시되지 않았습니다.")
    except Exception as e:
        print(f"🗙 팝업 처리 중 예외발생, 스킵하고 진행합니다:{e}")

    page.wait_for_timeout(2000)  # 2초 대기

    """
    🟢 Step1 Shipping
    """
    # Save & Continue
    page.locator('button.base-btn.primary.medium.ng-star-inserted', log_if_not_found=False).click()
    page.wait_for_timeout(2000)  # 2초 대기

    # Verify Your Address 팝업 있으면 클릭 없으면 스킵
    try:
        popup_verify = page.locator('button.btn-black.btn-btm-main', has_text="Keep This Address", log_if_not_found=False)
        if popup_verify.is_visible() and popup_verify.count() > 0 and popup_verify.is_enabled():
            popup_verify.click()
            print("☑ Verify Your Address 팝업이 표시되었습니다.")
        else:
            print("☑ Verify Your Address 팝업이 표시되지 않았습니다.")
    except Exception as e:
        print(f"🗙 팝업 처리 중 예외발생, 스킵하고 진행합니다:{e}")

    """
    🟢 Step2 Payment
    """
    # Store Credit Edit 버튼이 있으면 0원으로 사용, 없으면 스킵
    Store_Credit_edit = page.locator('a.ng-tns-c3-3.ng-star-inserted', has_text="Edit")

    if Store_Credit_edit.count() > 0 and Store_Credit_edit.is_visible() and Store_Credit_edit.is_enabled():
        Store_Credit_edit.click()
        Store_Credit_input = page.locator('input.input-edit.ng-untouched.ng-pristine.ng-valid')
        Store_Credit_input.fill("")  # 먼저 input 클리어
        Store_Credit_input.fill("0")
        Store_Credit_Use = page.locator('button.base-btn.medium.btn-info')
        Store_Credit_Use.click()  # Use 버튼 클릭
        print("☑ Store Credit을 0원으로 변경 하였습니다.")
    else:
        print("🗙 Store Credit Edit 버튼이 없어 스킵합니다.")

    # Save & Continue
    page.locator('button.base-btn.primary.medium.ng-star-inserted').click()
    page.wait_for_timeout(2000)  # 2초 대기

     # 백업카드 팝업이 있으면 x버튼 클릭 없으면 스킵
    try:
        popup_backupcard = page.locator('div.modal__content__header__close', log_if_not_found=False)
        if popup_backupcard.is_visible() and popup_backupcard.count() > 0 and popup_backupcard.is_enabled():
            popup_backupcard.click()
            print("☑ Backup Card 팝업이 표시되었습니다.")
        else:
            print("☑ Backup Card 팝업이 표시되지 않았습니다.")
    except Exception as e:
        print(f"🗙 팝업 처리 중 예외발생, 스킵하고 진행합니다:{e}")

    # Save & Continue
    page.locator('button.base-btn.primary.medium.ng-star-inserted').click()
    page.wait_for_timeout(2000)  # 2초 대기

    """
    🟢 Step3_Order Review
    """
    # Submit Order
    submit_btn = page.locator('button.base-btn.primary.medium.ng-star-inserted', has_text="Submit Order")
    if submit_btn.is_visible() and submit_btn.is_enabled():
        submit_btn.click()
        print("☑ Submit Order 버튼 클릭됨")
    else:
        print("☑ Submit Order 버튼이 비활성화 또는 숨겨져 있음")
    page.wait_for_url("**/checkout/confirm/**", timeout=10000)  # 주문 완료 페이지로 이동할 때까지 대기

    order_confirm_url = page.url
    print(f"☑ order confirm URL: {order_confirm_url}")

    # 주문 성공 여부 판정
    expected_url = f"https://beta-mobile.fashiongo.net/checkout/confirm/{cart_id}"
    if order_confirm_url.startswith(expected_url):
        print(f"🅿 Card Id: '{cart_id}' 주문 성공")
    else:
        print("❌ 주문 실패")

    page.wait_for_timeout(2000)  # 네트워크/페이지 이동 대기

def MO_checkout_StoreCredit(page):
    '''
    모바일 checkout 함수, Cart 부터 시작 (비동기)
    '''
    # Checkout All Vendor 버튼 클릭 후 split-orders 페이지로 이동
    with page.expect_navigation(url="**/checkout/split-orders?cartId=**", timeout=20000) as nav_info:
        page.locator('button.checkout-btn.nclick').click()

    # 반드시 with 블록이 끝난 후에 URL을 가져와야 함!
    split_url = (nav_info.value).url if nav_info.value else page.url
    print(f"☑ split_url 원본: {split_url}")

    # URL에서 &fsv= 이하의 쿼리 파라미터는 제거 (cartId 추출에 불필요한 부분 제거)
    if '&fsv=' in split_url:
        split_url = split_url.split('&fsv=')[0]
    print(f"☑ split_url: {split_url}")

    # 정규 표현식으로 split_url에서 cartId 값을 추출
    match = re.search(r'cartId=([a-z0-9\-]+)', split_url)
    cart_id = match.group(1) if match else None
    print(f"☑ cartId: {cart_id}")

    # You Have Promotions! 팝업 있으면 클릭 없으면 스킵
    try:
        popup_promotion = page.locator('button.btn-sure', has_text="Continue To Checkout", log_if_not_found=False)
        if popup_promotion.is_visible() and popup_promotion.count() > 0 and popup_promotion.is_enabled():
            popup_promotion.click()
            print("☑ You Have Promotions! 팝업이 표시되었습니다.")
        else:
            print("☑ You Have Promotions! 팝업이 표시되지 않았습니다.")
    except Exception as e:
        print(f"☑ 팝업 처리 중 예외발생, 스킵하고 진행합니다:{e}")

    page.wait_for_timeout(2000)  # 2초 대기

    """
    🟢 Step1 Shipping
    """
    # Save & Continue
    page.locator('button.base-btn.primary.medium.ng-star-inserted', log_if_not_found=False).click()
    page.wait_for_timeout(2000)  # 2초 대기

    # Verify Your Address 팝업 있으면 클릭 없으면 스킵
    try:
        popup_verify = page.locator('button.btn-black.btn-btm-main', has_text="Keep This Address", log_if_not_found=False)
        if popup_verify.is_visible() and popup_verify.count() > 0 and popup_verify.is_enabled():
            popup_verify.click()
            print("☑ Verify Your Address 팝업이 표시되었습니다.")
        else:
            print("☑ Verify Your Address 팝업이 표시되지 않았습니다.")
    except Exception as e:
        print(f"☑ 팝업 처리 중 예외발생, 스킵하고 진행합니다:{e}")

    """
    🟢 Step2 Payment
    """

    # Store Credit 설정
    Store_Credit_edit = page.locator('a.ng-star-inserted', has_text="Edit")

    if Store_Credit_edit.count() > 0 and Store_Credit_edit.is_visible() and Store_Credit_edit.is_enabled():
        Store_Credit_edit.click()
        Store_Credit_input = page.locator('input.input-edit')
        Store_Credit_input.fill("")  # input 클리어
        import random
        random_amount = random.randint(10, 200)
        Store_Credit_input.fill(str(random_amount))
        Store_Credit_Use = page.locator('button.base-btn.medium.btn-info')
        Store_Credit_Use.click()  # Use 버튼 클릭
        print(f"☑ Store Credit 입력값: {random_amount} Credit")
    else:
        print("🗙 Store Credit Edit 버튼이 없어 스킵합니다.")

    # Save & Continue
    page.locator('button.base-btn.primary.medium.ng-star-inserted').click()
    page.wait_for_timeout(2000)  # 2초 대기

     # 백업카드 팝업이 있으면 x버튼 클릭 없으면 스킵
    try:
        popup_backupcard = page.locator('div.modal__content__header__close', log_if_not_found=False)
        if popup_backupcard.is_visible() and popup_backupcard.count() > 0 and popup_backupcard.is_enabled():
            popup_backupcard.click()
            print("☑ Backup Card 팝업이 표시되었습니다.")
        else:
            print("☑ Backup Card 팝업이 표시되지 않았습니다.")
    except Exception as e:
        print(f"🗙 팝업 처리 중 예외발생, 스킵하고 진행합니다:{e}")

    # Save & Continue
    page.locator('button.base-btn.primary.medium.ng-star-inserted').click()
    page.wait_for_timeout(2000)  # 2초 대기

    """
    🟢 Step3_Order Review
    """
    # Submit Order
    submit_btn = page.locator('button.base-btn.primary.medium.ng-star-inserted', has_text="Submit Order")
    if submit_btn.is_visible() and submit_btn.is_enabled():
        submit_btn.click()
        print("☑ Submit Order 버튼 클릭됨")
    else:
        print("🗙 Submit Order 버튼이 비활성화 또는 숨겨져 있음")
    page.wait_for_url("**/checkout/confirm/**", timeout=10000)  # 주문 완료 페이지로 이동할 때까지 대기

    order_confirm_url = page.url
    print(f"☑ order confirm URL: {order_confirm_url}")

    # 주문 성공 여부 판정
    expected_url = f"https://beta-mobile.fashiongo.net/checkout/confirm/{cart_id}"
    if order_confirm_url.startswith(expected_url):
        print(f"🅿 Card Id: '{cart_id}' 주문 성공")
    else:
        print("❌ 주문 실패")

    page.wait_for_timeout(2000)  # 네트워크/페이지 이동 대기

def Order_detail_cancel(page):
    import pytest
    
    page.wait_for_timeout(2000)  # 네트워크/페이지 이동 대기
    # Cancel Order 버튼 찾기 및 클릭
    cancel_order = page.locator('button.link-cancel', has_text="CANCEL ORDER")
    
    try:
        # 버튼 대기 및 준비
        cancel_order.scroll_into_view_if_needed()
        cancel_order.focus()
        page.wait_for_timeout(500)
        
        # 네트워크 안정화 대기
        # page.wait_for_load_state('networkidle', timeout=5000)
        page.wait_for_timeout(1000)
    
        # 여러 방식으로 클릭 시도
        try:
            # 방법1: 일반 클릭
            cancel_order.click(timeout=3000)
            print("☑ CANCEL ORDER 버튼 클릭 성공 (일반 클릭)")
        except:
            # 방법2: force 클릭
            try:
                cancel_order.click(force=True, timeout=3000)
                print("☑ CANCEL ORDER 버튼 클릭 성공 (force 클릭)")
            except:
                # 방법3: JS 이벤트 디스패치
                cancel_order.evaluate("""
                    el => {
                        el.dispatchEvent(new MouseEvent('mousedown', {bubbles:true}));
                        el.dispatchEvent(new MouseEvent('mouseup', {bubbles:true}));
                        el.dispatchEvent(new MouseEvent('click', {bubbles:true}));
                        el.click();
                    }
                """)
                print("☑ CANCEL ORDER 버튼 클릭 성공 (JS 이벤트)")
        
        # 클릭 후 충분히 대기
        page.wait_for_timeout(2000)
        
        try:
                yes_button = page.locator('span.alert-button-inner', has_text="Yes")
                yes_button.wait_for(state='visible', timeout=10000)
                yes_button.click()
                print("☑ Cancel Confirmation 팝업의 Yes 버튼 클릭 성공")
        except Exception as popup_e:
            page.screenshot(path="output/cancel_popup_fail.png")
            pytest.fail(f"❌ Cancel Confirmation 팝업 또는 Yes 버튼을 찾지 못했습니다: {popup_e}")
            
    except Exception as e:
        page.screenshot(path="output/cancel_order_fail.png")
        pytest.fail(f"❌ CANCEL ORDER 클릭 실패: {e}")
