async def wa_login(page, account="wa2", logs=None):
    # logs가 None이면 빈 리스트로 초기화
    from core.page_account import LOGIN_CREDENTIALS

    # 로그를 저장할 리스트
    if logs is None:
        logs = []

    # 키 이름 생성
    username_key = f"{account}_username"
    password_key = f"{account}_password"

    # 로그인 정보 가져오기
    try:
        username = LOGIN_CREDENTIALS[username_key]
        password = LOGIN_CREDENTIALS[password_key]
    except KeyError as e:
        raise ValueError(f"LOGIN_CREDENTIALS {e} 키가 없습니다.")

    # 해당 정의 사용자 이름과 비번이 없을 경우 예외처리
    if not username or not password:
        raise ValueError(f"LOGIN_CREDENTIALS {account}가 없습니다.") 
    # raise의 의미: "예외를 던지다" 또는 "에러를 발생시키다"프로그램 실행을 중단하고 에러를 알림
    # 프로그램 실행을 중단하고 에러를 알림
    
    # 로그인 요소 정의 및 동작
    username_input = page.locator('#username') 
    await username_input.fill(username) # fill로 한번에 입력
    password_input = page.locator('#password')
    await password_input.fill(password)

    # login 버튼 클릭
    await page.locator('button.btn-login', has_text="Member Login").click()
    logs.append("로그인 완료")
    print(f"☑ WA_{account} 계정 로그인 완료")
    
    

