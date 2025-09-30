import random

# 전역에서 사용할 공통 함수 정의
async def checkout_process(page):
    """
    Cart 부터 시작
    """
    # Shopping BAG 클릭 후 URL 검증
    expected_url = 'https://beta-www.fashiongo.net/cart'
    await page.wait_for_url(expected_url)

    assert page.url == expected_url, f"Fail: Expected URL {expected_url}, but got {page.url}."
    print(f"Success: {expected_url} matched the expected value!")

    # Cart > Proceed To Checkout 버튼 클릭
    await page.locator('.btn-dark_grey.btn-checkoutAll.nclick').click()

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

    """
    🟢 Step1 Shipping
    """
    await page.locator('button.btn-dark_grey.btn-goToPayment.nclick').click()
    
    # Verify Your Address 팝업 있으면 클릭 없으면 스킵
    try:
        popup_verify = page.locator_popup('.common-btn.c-black', has_text="Keep This Address")
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
    await page.locator('button.btn-dark_grey.btn-goToReview.nclick').click()

    """
    🟢 Order Review
    """
    await page.locator('button.btn-dark_grey.btn-checkout.nclick').click()

    # 주문 완료 후 Thank you for your order! 텍스트가 포함된 h2 요소 확인
    await page.wait_for_load_state('networkidle')
    if await page.locator('h2.order-title').count() > 0:
        print("Order successful! Test passed.")
    else:
        print("Order not found! Test failed.")

async def checkout_promotion(page):
    """
    Cart 부터 시작
    """
    expected_url = 'https://beta-www.fashiongo.net/cart'
    await page.wait_for_url(expected_url)

    assert page.url == expected_url, f"Fail: Expected URL {expected_url}, but got {page.url}."
    print(f"Success: {expected_url} matched the expected value!")

    # Cart > Select Vendor Promotions 버튼 클릭(Vendor ID 16502 Allium)
    # await page.locator('button.btn-vendor.size-medium_blue[data-nclick-extra*="vid=16502"]').click()
    # 60% Off & Free Shipping $50.00+ Orders
    # await page.locator('button.btn-coupon-apply').first.click()

    # Cart > Proceed To Checkout 버튼 클릭
    await page.locator('.btn-dark_grey.btn-checkoutAll.nclick').click()

    # You Have Promotions! 팝업
    await page.locator_popup('button.btn-sure', has_text="Continue To Checkout")

    if await page.locator('button.btn-sure').count() > 0 and await page.locator('button.btn-sure').is_visible():
        await page.locator('button.btn-sure').click()
        print("You Have Promotions! 팝업이 표시되었습니다.")
    else:
        print("You Have Promotions! 팝업이 표시되지 않았습니다.")

    """
    🟢 Step1 Shipping
    """
    await page.locator('button.btn-dark_grey.btn-goToPayment.nclick').click()
    
    popup_verify = page.locator_popup('.common-btn.c-black', has_text="Keep This Address")

    if await popup_verify.is_visible() and await popup_verify.count() > 0 and await popup_verify.is_enabled():
        await popup_verify.click()
        print("Verify Your Address 팝업이 표시되었습니다.")
    else:
        print("Verify Your Address 팝업이 표시되지 않았습니다.")    

    """
    🟢 Step2 Payment
    """
    await page.locator('button.btn-dark_grey.btn-goToReview.nclick').click()

    """
    🟢 Order Review
    """
    await page.locator('button.btn-dark_grey.btn-checkout.nclick').click()

    await page.wait_for_load_state('networkidle')
    if await page.locator('h2.order-title').count() > 0:
        print("Order successful! Test passed.")
    else:
        print("Order not found! Test failed.")

# Create Items
async def va_Create_items(page, image_prefix="", size="", pack=""):
    from random import sample, randint
    import os

    random_number = random.randint(1,999)

    # 2. Active/Inactive 라디오버튼 locator
    active_radio = page.locator('input[type="radio"][ng-reflect-value="true"]')
    inactive_radio = page.locator('input[type="radio"][ng-reflect-value="false"]')

    # 3. Active가 체크 안 되어 있으면
    if not await active_radio.first.is_checked():
        label = active_radio.first.locator('..')
        await label.click(force=True)
        await page.wait_for_timeout(300)
        if not await active_radio.first.is_checked():
            await active_radio.first.evaluate("""
                el => {
                    el.checked = true;
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                }
            """)
            await page.wait_for_timeout(300)
            if await active_radio.first.is_checked():
                print("☑ JS로 Active checked 상태 됨")
            else:
                print("❌ JS로도 Active checked 안 됨")
        else:
            print("☑ label 클릭 후 Active checked 상태 됨")
    else:
        print("☑ 이미 Active checked 상태")

    if await inactive_radio.first.is_checked():
        print("❌ 여전히 Inactive checked 상태임")

    # Style No 입력
    input_styleNo = page.locator('input[formcontrolname="productName"]')
    await input_styleNo.click()
    await input_styleNo.type(f"AutoSN-{image_prefix}{random_number}", delay=50)

    # Item Name 입력
    input_ItemName = page.locator('input[formcontrolname="itemName"]')
    await input_ItemName.click()
    await input_ItemName.type(f"Auto_{image_prefix}{random_number}", delay=50)

    await page.select_option('select[formcontrolname="selCat1"]', label="Women's Apparel")
    await page.select_option('select[formcontrolname="selCat2"]', label="Tops")
    await page.select_option('select[formcontrolname="selCat3"]', label="Graphic T-shirts")

    await page.locator('textarea[formcontrolname="description"]').type('Write Description!', delay=50)

    random_price = str(random.randint(10,101))
    price = page.locator('input[formcontrolname="sellingPrice"]')
    await price.type(random_price, delay=50)
    print(f"price ${random_price}로 입력 했습니다.")

    await page.select_option('select[formcontrolname="sizeId"]', label=size)
    await page.select_option('select[formcontrolname="packId"]', label=pack)

    await page.locator('a.view-color-list-btn').click()
    await page.wait_for_timeout(1000)

    from random import sample

    checkbox_divs = page.locator("div.check-square")
    checkbox_count = await checkbox_divs.count()
    print(f"☑ 클릭 가능한 Color 체크박스 수: {checkbox_count} 개")

    visible_indices = [i for i in range(checkbox_count) if await checkbox_divs.nth(i).is_visible()]

    if len(visible_indices) < 2:
        print("화면에 보이는 체크박스가 2개 미만 입니다.")
        random_indices = []
    else:
        number_select = random.randint(2, min(5, len(visible_indices)))
        random_indices = random.sample(visible_indices, number_select)

    for i in random_indices:
        checkbox_div = checkbox_divs.nth(i)
        await checkbox_div.click()
        print(f"✔ div.check-square #{i} 클릭 시도")

    await page.locator('i.btn-close').click()
    await page.wait_for_timeout(3000)

    input_selector = 'input[type="file"][name="multiple"]'
    await page.eval_on_selector(input_selector, 'el => el.style.display = "block"')

    # 이미지 파일 url로 가져와서 output에 저장한 다음에 업로드 하도록 추가
    image_dir = 'C:\\playwright\\autoplay\\fg_image'
    image_paths = [
        os.path.join(image_dir, f'{image_prefix}{i}.png')
        for i in range(1, 3)
        if os.path.exists(os.path.join(image_dir, f'{image_prefix}{i}.png'))]

    if not image_paths:
        print("❌ 이미지 파일 없음.")
        return

    await page.set_input_files(input_selector, image_paths)

    for image_path in image_paths:
        print(f"☑ 이미지 업로드 완료: {image_path}")
    await page.wait_for_timeout(3000)

    save_button = page.locator("button.btn-blue", has_text="Save").first
    await save_button.wait_for(state="visible")
    def is_item_create_response(response):
        return (
            "item" in response.url and
            response.request.method == "POST"
        )
    async with page.expect_response(is_item_create_response) as resp_info:
        await save_button.click()

    response = await resp_info.value
    try:
        data = await response.json()
        print("XHR 응답 데이터:", data)
        product_id = data.get("data")
        
        openpack_product_id = None
        prepack_product_id = None

        if image_prefix.lower() == "openpack":
            openpack_product_id = product_id
            print("생성된 OpenPack productId:", openpack_product_id)
            with open("created_openpack_id.txt", "w") as f:
                f.write(str(openpack_product_id))
        elif image_prefix.lower() == "prepack":
            prepack_product_id = product_id
            print("생성된 PrePack productId:", prepack_product_id)
            with open("created_prepack_id.txt", "w") as f:
                f.write(str(prepack_product_id))
        else:
            print(f"알 수 없는 prefix '{image_prefix}'의 productId:", product_id)

    except Exception as e:
        print("응답 파싱 실패:", e)
        product_id = None
        openpack_product_id = None
        prepack_product_id = None

    await page.wait_for_timeout(3000)
    print(f"Auto_item{random_number} 생성이 완료 되었습니다.")

    return {
        "product_id": product_id,
        "openpack_product_id": openpack_product_id if image_prefix.lower() == "openpack" else None,
        "prepack_product_id": prepack_product_id if image_prefix.lower() == "prepack" else None,
    }