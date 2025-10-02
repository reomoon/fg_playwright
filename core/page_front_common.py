import random

# 전역에서 사용할 공통 함수 정의
def checkout_process(page):
    """
    Cart 부터 시작
    """
    # Shopping BAG 클릭 후 URL 검증
    expected_url = 'https://beta-www.fashiongo.net/cart'
    page.wait_for_url(expected_url)

    assert page.url == expected_url, f"Fail: Expected URL {expected_url}, but got {page.url}."
    print(f"🅿 Success: {expected_url} matched the expected value!")

    # Cart > Proceed To Checkout 버튼 클릭
    page.locator('.btn-dark_grey.btn-checkoutAll.nclick').click()

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

    """
    🟢 Step1 Shipping
    """
    page.locator('button.btn-dark_grey.btn-goToPayment.nclick').click()
    
    # Verify Your Address 팝업 있으면 클릭 없으면 스킵
    try:
        popup_verify = page.locator('.common-btn.c-black', has_text="Keep This Address", log_if_not_found=False)
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
    page.locator('button.btn-dark_grey.btn-goToReview.nclick').click()

    """
    🟢 Order Review
    """
    page.locator('button.btn-dark_grey.btn-checkout.nclick').click()

    # 주문 완료 후 Thank you for your order! 텍스트가 포함된 h2 요소 확인
    page.wait_for_load_state('networkidle')
    if page.locator('h2.order-title').count() > 0:
        print("Order successful! Test passed.")
    else:
        print("Order not found! Test failed.")

def checkout_promotion(page):
    """
    Cart 부터 시작
    """
    expected_url = 'https://beta-www.fashiongo.net/cart'
    page.wait_for_url(expected_url)

    assert page.url == expected_url, f"Fail: Expected URL {expected_url}, but got {page.url}."
    print(f"Success: {expected_url} matched the expected value!")

    # Cart > Select Vendor Promotions 버튼 클릭(Vendor ID 16502 Allium)
    # page.locator('button.btn-vendor.size-medium_blue[data-nclick-extra*="vid=16502"]').click()
    # 60% Off & Free Shipping $50.00+ Orders
    # page.locator('button.btn-coupon-apply').first.click()

    # Cart > Proceed To Checkout 버튼 클릭
    page.locator('.btn-dark_grey.btn-checkoutAll.nclick').click()

    # You Have Promotions! 팝업
    page.locator('button.btn-sure', has_text="Continue To Checkout")

    if page.locator('button.btn-sure').count() > 0 and page.locator('button.btn-sure').is_visible():
        page.locator('button.btn-sure').click()
        print("☑ You Have Promotions! 팝업이 표시되었습니다.")
    else:
        print("☑ You Have Promotions! 팝업이 표시되지 않았습니다.")

    """
    🟢 Step1 Shipping
    """
    page.locator('button.btn-dark_grey.btn-goToPayment.nclick').click()
    
    popup_verify = page.locator('.common-btn.c-black', has_text="Keep This Address", log_if_not_found=False)

    if popup_verify.is_visible() and popup_verify.count() > 0 and popup_verify.is_enabled():
        popup_verify.click()
        print("☑ Verify Your Address 팝업이 표시되었습니다.")
    else:
        print("☑ Verify Your Address 팝업이 표시되지 않았습니다.")    

    """
    🟢 Step2 Payment
    """
    page.locator('button.btn-dark_grey.btn-goToReview.nclick').click()

    """
    🟢 Order Review
    """
    page.locator('button.btn-dark_grey.btn-checkout.nclick').click()

    page.wait_for_load_state('networkidle')
    if page.locator('h2.order-title').count() > 0:
        print("☑ Order successful! Test passed.")
    else:
        print("☑ Order not found! Test failed.")

# Create Items
def va_Create_items(page, image_prefix="", size="", pack=""):
    from random import sample, randint
    import os

    random_number = random.randint(1,999)

    # 2. Active/Inactive 라디오버튼 locator
    active_radio = page.locator('input[type="radio"][ng-reflect-value="true"]')
    inactive_radio = page.locator('input[type="radio"][ng-reflect-value="false"]')

    # 3. Active가 체크 안 되어 있으면
    if not active_radio.first.is_checked():
        label = active_radio.first.locator('..')
        label.click(force=True)
        page.wait_for_timeout(300)
        if not active_radio.first.is_checked():
            active_radio.first.evaluate("""
                el => {
                    el.checked = true;
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                }
            """)
            page.wait_for_timeout(300)
            if active_radio.first.is_checked():
                print("☑ JS로 Active checked 상태 됨")
            else:
                print("❌ JS로도 Active checked 안 됨")
        else:
            print("☑ label 클릭 후 Active checked 상태 됨")
    else:
        print("☑ 이미 Active checked 상태")

    if inactive_radio.first.is_checked():
        print("❌ 여전히 Inactive checked 상태임")

    # Style No 입력
    input_styleNo = page.locator('input[formcontrolname="productName"]')
    input_styleNo.click()
    input_styleNo.type(f"AutoSN-{image_prefix}{random_number}", delay=50)

    # Item Name 입력
    input_ItemName = page.locator('input[formcontrolname="itemName"]')
    input_ItemName.click()
    input_ItemName.type(f"Auto_{image_prefix}{random_number}", delay=50)

    page.select_option('select[formcontrolname="selCat1"]', label="Women's Apparel")
    page.select_option('select[formcontrolname="selCat2"]', label="Tops")
    page.select_option('select[formcontrolname="selCat3"]', label="Graphic T-shirts")

    page.locator('textarea[formcontrolname="description"]').type('Write Description!', delay=50)

    random_price = str(random.randint(10,101))
    price = page.locator('input[formcontrolname="sellingPrice"]')
    price.type(random_price, delay=50)
    print(f"☑ price ${random_price}로 입력 했습니다.")

    page.select_option('select[formcontrolname="sizeId"]', label=size)
    page.select_option('select[formcontrolname="packId"]', label=pack)

    page.locator('a.view-color-list-btn').click()
    page.wait_for_timeout(1000)

    from random import sample

    checkbox_divs = page.locator("div.check-square")
    checkbox_count = checkbox_divs.count()
    print(f"☑ 클릭 가능한 Color 체크박스 수: {checkbox_count} 개")

    visible_indices = [i for i in range(checkbox_count) if checkbox_divs.nth(i).is_visible()]

    if len(visible_indices) < 2:
        print("☑ 화면에 보이는 체크박스가 2개 미만 입니다.")
        random_indices = []
    else:
        number_select = random.randint(2, min(5, len(visible_indices)))
        random_indices = random.sample(visible_indices, number_select)

    for i in random_indices:
        checkbox_div = checkbox_divs.nth(i)
        checkbox_div.click()
        print(f"☑ div.check-square #{i} 클릭 시도")

    page.locator('i.btn-close').click()
    page.wait_for_timeout(3000)

    input_selector = 'input[type="file"][name="multiple"]'
    page.eval_on_selector(input_selector, 'el => el.style.display = "block"')

    # 이미지 파일 url로 가져와서 output에 저장한 다음에 업로드 하도록 추가
    image_dir = 'C:\\playwright\\fg_playwright\\output'
    image_paths = [
        os.path.join(image_dir, f'{image_prefix}{i}.png')
        for i in range(1, 3)
        if os.path.exists(os.path.join(image_dir, f'{image_prefix}{i}.png'))]

    if not image_paths:
        print("❌ 이미지 파일 없음.")
        return

    page.set_input_files(input_selector, image_paths)

    for image_path in image_paths:
        print(f"☑ 이미지 업로드 완료: {image_path}")
    page.wait_for_timeout(3000)

    save_button = page.locator("button.btn-blue", has_text="Save").first
    save_button.wait_for(state="visible")
    def is_item_create_response(response):
        return (
            "item" in response.url and
            response.request.method == "POST"
        )
    with page.expect_response(is_item_create_response) as resp_info:
        save_button.click()

    response = resp_info.value
    try:
        data = response.json()
        print("☑ XHR 응답 데이터:", data)
        product_id = data.get("data")
        
        openpack_product_id = None
        prepack_product_id = None

        if image_prefix.lower() == "openpack":
            openpack_product_id = product_id
            print("생성된 OpenPack productId:", openpack_product_id)
            with open("output\\created_openpack_id.txt", "w") as f:
                f.write(str(openpack_product_id))
        elif image_prefix.lower() == "prepack":
            prepack_product_id = product_id
            print("생성된 PrePack productId:", prepack_product_id)
            with open("output\\created_prepack_id.txt", "w") as f:
                f.write(str(prepack_product_id))
        else:
            print(f"알 수 없는 prefix '{image_prefix}'의 productId:", product_id)

    except Exception as e:
        print("응답 파싱 실패:", e)
        product_id = None
        openpack_product_id = None
        prepack_product_id = None

    page.wait_for_timeout(3000)
    print(f"🅿 Auto_item{random_number} 생성이 완료 되었습니다.")

    return {
        "product_id": product_id,
        "openpack_product_id": openpack_product_id if image_prefix.lower() == "openpack" else None,
        "prepack_product_id": prepack_product_id if image_prefix.lower() == "prepack" else None,
    }