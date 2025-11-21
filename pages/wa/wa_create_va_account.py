from core.page_wrapper import HighlightPageWrapper
from core.close_by_close_buttons import close_by_close_buttons

def create_vendor_account(page):
    vendor_account = "alliumtest" # 벤더 ID

    # 팝업이 뜨기 전에 Net Terms 온보딩 쿠키 추가
    page.context.add_cookies([{
        "name": "hideBalanceOnboardingPopup",
        "value": "true",
        "domain": "beta-vendoradmin.fashiongo.net",
        "path": "/"
    }])
    print("☑ Net Terms 온보딩 쿠키")

    # 쿠키 적용을 위해 새로고침
    page.reload()

    # Go To Vendor Admin 클릭 새 탭 열림
    with page.context.expect_page() as new_page_into: # 새 탭이 열릴때까지 기다림
        page.locator('a.header__userinfo__user-info__wholesale', has_text="VENDOR ADMIN").click()

    vendor_page = new_page_into.value # 새로 열린 페이지 비동기로 객체 지정
    vendor_page.set_viewport_size({"width": 1680, "height": 900}) # 화면 사이즈 조절

    # vendor list 화면 company name 요소 나올 때까지 기다리기
    vendor_page.wait_for_selector('select', timeout=90000) # timeout 90초

    # 검색 > Ctrl + F (Windows 기준)
    vendor_page.keyboard.down('Control')
    vendor_page.keyboard.press('f')
    vendor_page.keyboard.up('Control')

    # 검색 > "allium" 입력
    vendor_page.keyboard.type("allium", delay=50)    
    vendor_page.locator('div.vendor-name', has_text="Allium").click()
    print("☑ allium vendor 검색하여 클릭")

    # Account 메뉴 클릭
    # 1."Account"가 보이면 클릭
    vendor_page.locator('span.txt-info', has_text="Account").wait_for(state="visible", timeout=5000)
    vendor_page.locator('span.txt-info', has_text="Account").click()

    # 2."Account Setting" 항목 보일 때 까지 기다린 후 클릭
    vendor_page.locator("p.sub-ttl", has_text="Account Setting").wait_for(state="visible", timeout=5000)
    vendor_page.locator("p.sub-ttl", has_text="Account Setting").click()

    # 3."Manage Account" 보일 때 까지 기다린 후 클릭
    manage_account = vendor_page.locator("a", has_text="Manage Account")
    manage_account.wait_for(state="visible", timeout=5000)
    manage_account.click()

    # allium1 계정이 있는지 확인
    if vendor_page.locator("td", has_text=vendor_account).count() > 0:
        print(f"{vendor_account} 계정이 있습니다. 해당 케이스를 종료 합니다.")
        return # 더 이상 실행하지 않고 종료
    else:
        print(f"{vendor_account} 계정 생성 진행 중...")

    """
    Add a New Account > Allium 계정 생성
    """
    # + Add New Account 클릭
    vendor_page.locator('a.link.link-light', has_text="Add New Account").click()

    # First & Last Name 입력
    vendor_page.locator('input[formcontrolname="firstName"]').type("Beta", delay=50)
    vendor_page.locator('input[formcontrolname="lastName"]').type(vendor_account, delay=50)

    # User ID / Password
    vendor_page.locator('input[formcontrolname="userId"]').type(vendor_account, delay=50)
    vendor_page.locator('input[formcontrolname="password"]').type("789456123qQ!", delay=50)

    vendor_page.wait_for_timeout(3000) # 3초 대기
    
    # 권한 체크 요소 찾기
    checkboxs = vendor_page.locator('li >> div.check-square')

    # 전체 체크박스 개수 확인
    count = checkboxs.count()

    for i in range(count):
        # i 번째 체크박스 요소 가져오기
        checkbox = checkboxs.nth(i)

        # 해당 체크박스 클릭
        checkbox.click()  

    # Save 버튼 클릭
    vendor_page.locator('button.btn.btn-blue', has_text="Save").click()
    vendor_page.wait_for_timeout(3000) #저장 후 3초 대기

    # allium1 계정이 있으면 성공
    if vendor_page.locator("td", has_text=vendor_account).count() > 0:
        print(f"🅿 '{vendor_account}' account created successfully.")
    else:
        print(f"❌ '{vendor_account}' account creation failed.")