from core.page_wrapper import HighlightPageWrapper
from core.close_by_close_buttons import close_by_close_buttons

def create_vendor_account(page, logs=None):
    """
    wa_login_token에서 받은 page로 바로 벤더 계정 생성
    """
    if logs is None:
        logs = []

    vendor_account = "alliumtest"  # 벤더 ID

    # 팝업이 뜨기 전에 Net Terms 온보딩 쿠키 추가
    page.context.add_cookies([{
        "name": "hideBalanceOnboardingPopup",
        "value": "true",
        "domain": "beta-vendoradmin.fashiongo.net",
        "path": "/"
    }])
    print("☑ Net Terms 온보딩 쿠키 추가")

    # 검색 > Ctrl + F (Windows 기준)
    page.keyboard.down('Control')
    page.keyboard.press('f')
    page.keyboard.up('Control')

    # 검색 > "allium" 입력
    page.keyboard.type("allium", delay=50)    
    page.locator('div.vendor-name', has_text="Allium").click()
    print("☑ allium vendor 검색하여 클릭")

    # Account 메뉴 클릭
    page.locator('span.txt-info', has_text="Account").wait_for(state="visible", timeout=5000)
    page.locator('span.txt-info', has_text="Account").click()

    # Account Setting 클릭
    page.locator("p.sub-ttl", has_text="Account Setting").wait_for(state="visible", timeout=5000)
    page.locator("p.sub-ttl", has_text="Account Setting").click()

    # Manage Account 클릭
    manage_account = page.locator("a", has_text="Manage Account")
    manage_account.wait_for(state="visible", timeout=5000)
    manage_account.click()

    # alliumtest 계정이 있는지 확인
    page.wait_for_timeout(3000)
    if page.locator("td", has_text=vendor_account).count() > 0:
        print(f"{vendor_account} 계정이 있습니다. 해당 케이스를 종료합니다.")
        logs.append(f"{vendor_account} 계정 이미 존재")
        return logs

    print(f"{vendor_account} 계정 생성 진행 중...")

    # + Add New Account 클릭
    page.locator('a.link.link-light', has_text="Add New Account").click()

    # First & Last Name 입력
    page.locator('input[formcontrolname="firstName"]').type("Beta", delay=50)
    page.locator('input[formcontrolname="lastName"]').type(vendor_account, delay=50)

    # User ID / Password
    page.locator('input[formcontrolname="userId"]').type(vendor_account, delay=50)
    page.locator('input[formcontrolname="password"]').type("789456123qQ!", delay=50)

    page.wait_for_timeout(3000)
    
    # 권한 체크 요소 찾기
    checkboxs = page.locator('li >> div.check-square')
    count = checkboxs.count()

    for i in range(count):
        checkbox = checkboxs.nth(i)
        checkbox.click()  

    # Save 버튼 클릭
    page.locator('button.btn.btn-blue', has_text="Save").click()
    page.wait_for_timeout(3000)

    # 계정 생성 확인
    if page.locator("td", has_text=vendor_account).count() > 0:
        print(f"🅿 '{vendor_account}' account created successfully.")
        logs.append(f"'{vendor_account}' 계정 생성 완료")
    else:
        print(f"❌ '{vendor_account}' account creation failed.")
        logs.append(f"'{vendor_account}' 계정 생성 실패")

    return logs