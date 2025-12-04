from core.page_account import LOGIN_CREDENTIALS

def wa_login_token(page, account="wa2"):
    """
    WA 로그인 후 JWT 토큰으로 Vendor Admin 페이지로 이동
    """
    username_key = f"{account}_username"
    password_key = f"{account}_password"

    try:
        username = LOGIN_CREDENTIALS[username_key]
        password = LOGIN_CREDENTIALS[password_key]
    except KeyError as e:
        raise ValueError(f"LOGIN_CREDENTIALS {e} 키가 없습니다.")

    if not username or not password:
        raise ValueError(f"LOGIN_CREDENTIALS {account}가 없습니다.")
    
    # 1. WA 로그인 페이지로 이동
    page.goto("https://beta-webadmin.fashiongo.net/login")
    page.wait_for_timeout(2000)
    
    # 2. 로그인
    page.locator('#username').fill(username)
    page.locator('#password').fill(password)
    page.locator('button.btn-login', has_text="Member Login").click()
    page.wait_for_timeout(3000)
    
    print(f"☑ WA_{account} 계정 로그인 완료")

    # 3. 쿠키에서 tokenID 추출
    cookies = page.context.cookies()
    print(f"🅿 저장된 쿠키: {len(cookies)}개")
    
    auth_token = None
    for cookie in cookies:
        print(f"  - {cookie['name']}: {cookie['value'][:30]}...")
        if cookie['name'] == 'tokenID':
            auth_token = cookie['value']
            print(f"✅ tokenID 찾음: {auth_token[:50]}...")
            break

    if not auth_token:
        print("❌ 쿠키에서 tokenID를 찾을 수 없습니다.")
        raise ValueError("JWT 토큰 추출 실패")

    # 4. JWT 토큰으로 Vendor Admin 페이지로 이동
    print(f"🅿 인증 토큰 획득 완료: {auth_token[:50]}...")
    vendor_admin_url = f"https://beta-vendoradmin.fashiongo.net/#/auth/webadmin/login/{auth_token}"
    print(f"☑ Vendor Admin 페이지로 이동")
    page.goto(vendor_admin_url)
    page.wait_for_timeout(3000)
    print(f"🅿 Vendor Admin 페이지 진입 완료")
    
    return page