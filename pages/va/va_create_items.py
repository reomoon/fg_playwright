from core.page_front_common import va_Create_items

# OpenPack Item
def va_create_items_openpack(page):  # Size, Pack 인수 지정
    menu_items = page.locator('div.nav__item__title', has_text="Items")
    menu_items.wait_for(state='visible', timeout=5000)  # 최대 5초 대기
    menu_items.click()

    # Items > Create a New Item 메뉴
    menu_NewItem = page.locator('a.nav__group__item__title', has_text="Create a New Item")
    menu_NewItem.wait_for(state='visible', timeout=5000)
    menu_NewItem.click()
    page.wait_for_timeout(3000)
    
    # 여기서 openpack용 값으로 직접 호출
    return va_Create_items(page, image_prefix="openpack", size="S-M-L", pack="Open-pack")
    # va_Create_items(page, size, pack) # va_create_items_openpack 함수 호출

# PrePack Item
def va_create_items_prepack(page):
    # Va > items 메뉴 클릭
    menu_items = page.locator('div.nav__item__title', has_text="Items")
    menu_items.wait_for(state='visible', timeout=5000)  # 최대 5초 대기
    menu_items.click()

    # Items > Create a New Item 메뉴
    menu_NewItem = page.locator('a.nav__group__item__title', has_text="Create a New Item")
    menu_NewItem.wait_for(state='visible', timeout=5000)
    menu_NewItem.click()
    page.wait_for_timeout(3000)

    # 여기서 prepack용 값으로 직접 호출
    return va_Create_items(page, image_prefix="prepack", size="S-M-L", pack="1-1-1")
   

# PrePack Item (XL 포함)
def va_create_items_prepack1(page):  # Size, Pack 인수 지정
    # Va > items 메뉴 클릭
    menu_items = page.locator('div.nav__item__title', has_text="Items")
    menu_items.wait_for(state='visible', timeout=5000)  # 최대 5초 대기
    menu_items.click()

    # Items > Create a New Item 메뉴
    menu_NewItem = page.locator('a.nav__group__item__title', has_text="Create a New Item")
    menu_NewItem.wait_for(state='visible', timeout=5000)
    menu_NewItem.click()
    page.wait_for_timeout(3000)

    # va_create_items_prepack 함수 호출
    return va_Create_items(page, image_prefix="prepack", size="S-M-L-XL", pack="2-2-2-2")