import os
import pytesseract            
from core.page_ocr import captcha_mobile_capture, remove_lines, perform_easyocr

# Tesseract-OCR 경로 설정 (윈도우 사용자만 필요)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Pages/front openpack order
def mo_create_card(page):
    """
    My Account > My Cards 이동
    """
    # 자동화 탐지 방지를 위한 HTTP 헤더 추가(goto 전에 설정)
    page.set_extra_http_headers({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    # Footer Bag 아이콘 선택
    page.locator('span.icon.account').click()
    print("☑ footer Account 버튼 클릭 성공")

    # /account 페이지 출력되면 성공
    page.wait_for_url("**/account", timeout=5000)
    if "/account" in page.url: # /account가 페이지 url안에 있으면
        print("☑ /account 페이지 진입 성공")
    else: # url이 없다면
        print("❌ /account 페이지 진입 실패")
        return False
    """
    카드 추가 여부에 따른 if문 실행
    """


    # My Card 메뉴 이동
    mycards_menu = page.locator('a[routerlink="/myaccount/mycard"]')
    mycards_menu.click()

    # Add New Card 버튼
    page.locator('p.add-new-card-con').click()

    # 웹폰트 로딩 대기
    page.evaluate("document.fonts.ready.then(() => console.log('모든 글꼴이 로드됨'))")

    # Name on Card 입력
    Name_on_Card = page.locator('ion-input[formcontrolname="name"] input')
    Name_on_Card.click()
    Name_on_Card.type('Home')

    # Card Number 입력
    Card_number = page.locator('input[name="cardnumber"]')
    Card_number.click()
    Card_number.fill('4242424242424242')

    for attempt in range(5):
        Card_number.fill("") # 입력란 초기화
        Card_number.fill("4242424242424242")
        entered_value = Card_number.input_value() # 입력 값 확인

        if entered_value.replace(" ","") == '4242424242424242': # 띄어쓰기 없애고, 4242 맞는지 확인
            print(f"☑ 카드번호가 정상 입력 되었습니다. ({attempt+1}번 째 시도)")
            break # 끝냄
        else:
            print(f"☒ 카드번호 입력이 잘못 되었습니다. {attempt+1}번 째 시도")
    else:
        print("❌ 카드번호 입력이 실패 하였습니다.")
    
    card_exp = page.locator('input[name="exp-date"]')
    card_exp.click()
    card_exp.type('0128', delay=100)
    card_secu_code = page.locator('input[name="cvc"')
    card_secu_code.click()
    card_secu_code.type('123', delay=100)
    card_zipcode = page.locator('input[name="postal"')
    card_zipcode.click()
    card_zipcode.type('11201')
    
    # 주소 정보 입력
    page.locator('ion-input[formcontrolname="address1"] input').type('38 Henry St')
    page.locator('ion-input[formcontrolname="city').type('Brooklyn')

    # 드롭다운에서 "New York" 옵션 선택
    page.locator('.select-text').select_option('New York')
    page.locator('ion-input[formcontrolname="zip').type('11201')
    # page.locator('#country').select_option('United States') # 드롭다운에서 United States" 옵션 선택 value 속성 사용

    # captcha 캡처 함수 불러오기
    captcha_mobile_capture(page)

    # output 폴더 경로 설정
    output_dir = os.path.join(os.getcwd(), "output")

    # 원본 이미지 경로 (output 폴더 내)
    input_image_path = os.path.join(output_dir, "captcha.png")

    # 선 제거 후 저장할 이미지 경로 (output 폴더 내)
    output_image_path = os.path.join(output_dir, "processed_captcha.png")

    # 선 제거
    remove_lines(input_image_path, output_image_path)
    
    # OCR 처리(인식하는데 좀 걸리지만 80%이상 성공)
    captcha_text = perform_easyocr(output_image_path)

    # 캡챠 입력
    page.locator('#card_captcha_answer').type(captcha_text)

    # Invalid Verification Code(Captcha) 팝업 처리 및 OCR 재시도
    for attempt in range(3):  # 최대 3번 시도
        # Save 버튼 클릭
        page.locator('.save-btn nclick').click()
        page.wait_for_timeout(3000)  # 3초 대기

        # 팝업 확인(log_if_not_found=False로 실제 팝업이 안나와도 ❌ 출력 안함)
        if page.locator('#close-showInfoError', log_if_not_found=False).is_visible():
            print(f"Invalid Verification Code 팝업 감지됨. OCR 재시도 중... (시도 {attempt + 1}/3)")
            # 팝업 닫기
            page.locator('#close-showInfoError').click()

            # 새로운 캡챠 이미지 캡처
            captcha_mobile_capture(page)

            # processed_captcha.png 파일이 있다면 기존 파일 삭제
            if os.path.exists(output_image_path):
                os.remove(output_image_path)

            # 새로 생성
            remove_lines(input_image_path, output_image_path)

            # 파일 생성 대기
            page.wait_for_timeout(500)
            
            # OCR 다시 수행
            captcha_text = perform_easyocr(output_image_path)

            # OCR 결과 검증
            if not captcha_text:
                print("☒ OCR 결과가 유효하지 않아 재시도합니다.")
                continue  # 다음 시도로 이동

            # 캡챠 입력
            page.locator('ion-input[formcontrolname="captchaAnswer"] input').fill("")  # 기존 입력값 초기화
            page.locator('ion-input[formcontrolname="captchaAnswer"] input').type(captcha_text)
        else:
            print("🅿 카드 추가 완료")
            break  # 팝업이 없으면 루프 종료
    else:
        print("❌ 최대 시도 횟수를 초과했습니다. 카드 추가 실패.")