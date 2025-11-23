import os
import pytesseract            
import pytest
from core.page_ocr import captcha_mobile_capture, remove_lines, perform_easyocr

# Tesseract-OCR 경로 설정 (윈도우 사용자만 필요)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Pages/front openpack order
def mo_add_new_card(page):
    """
    My Account > My Cards 이동
    """
    # /account 페이지 출력되면 성공
    # page.wait_for_url("**/account", timeout=5000)
    # if "/account" in page.url: # /account가 페이지 url안에 있으면
    #     print("☑ /account 페이지 진입 성공")
    # else: # url이 없다면
    #     print("🗙 /account 페이지 진입 실패")
    #     return False
    """
    카드 추가 여부에 따른 if문 실행
    """

    # My Card 메뉴 이동
    page.goto("https://beta-mobile.fashiongo.net/myaccount/mycard")
    page.wait_for_timeout(1000)
    print("☑ /myaccount/mycard 이동")

    # "VISA ending in 4242" 카드가 있는지 확인
    try:
        card_element = page.locator('p.card-num', has_text="VISA ending in 4242")
        if card_element.is_visible():
            print("🅿 VISA ending in 4242 카드가 이미 존재합니다.")
            return True
        else:
            print("☑ VISA ending in 4242 카드가 없습니다. 새로운 카드를 추가합니다.")
    except Exception as e:
        print(f"☑ 카드 확인 중 오류 발생: {e}. 새로운 카드를 추가합니다.")

    # Add New Card 버튼
    page.locator('p.add-new-card-con', log_if_not_found=False).click()

    # iframe으로 전환되었는지 확인 (Stripe 결제 폼의 경우)
    iframe = page.frame_locator('iframe[name^="__privateStripeFrame"]').first
    print(f"iframe 객체: {iframe}")
    
    # 웹폰트 로딩 대기
    page.evaluate("document.fonts.ready.then(() => console.log('모든 글꼴이 로드됨'))")
    page.wait_for_timeout(2000)  # 추가 대기

    # Name on Card 입력
    Name_on_Card = page.locator('ion-input[formcontrolname="name"] input')
    Name_on_Card.wait_for(state="visible", timeout=10000)
    Name_on_Card.click()
    Name_on_Card.type('Home')

    # iframe 내부로 진행
    Card_number = iframe.locator('input[name="cardnumber"]')
    Card_number.wait_for(state="visible", timeout=5000)
    Card_number.click()

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
    
    # iframe 내부의 카드 정보 입력 필드들
    card_exp = iframe.locator('input[name="exp-date"]')
    card_exp.click()
    card_exp.type('0128', delay=100)
    
    card_secu_code = iframe.locator('input[name="cvc"]')
    card_secu_code.click()
    card_secu_code.type('123', delay=100)
    
    card_zipcode = iframe.locator('input[name="postal"]')
    card_zipcode.click()
    card_zipcode.type('11201')
    
    # 주소 정보 입력
    page.locator('ion-input[formcontrolname="address1"] input').type('38 Henry St')
    page.locator('ion-input[formcontrolname="city"] input').type('Brooklyn')

    # "State" 드롭다운 아이콘 클릭
    page.locator('.select-icon').nth(0).click(force=True) # 첫 번째 클릭
    page.wait_for_timeout(500)  # 옵션 표시 대기

    # "New York" 옵션 클릭
    page.locator('div.alert-radio-label', has_text="New York").click()
    page.locator('span.alert-button-inner', has_text="OK").click()

    # Zip Code 입력
    page.locator('ion-input[formcontrolname="zip"] input').type('11201')

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
    page.locator('ion-input[formcontrolname="captchaAnswer"] input').type(captcha_text)

    # Invalid Verification Code(Captcha) 팝업 처리 및 OCR 재시도
    for attempt in range(3):  # 최대 3번 시도
        # Save 버튼 클릭
        page.locator('button.save-btn.nclick').click()
        page.wait_for_timeout(3000)  # 3초 대기

        # 팝업 확인(log_if_not_found=False로 실제 팝업이 안나와도 ❌ 출력 안함)
        if page.locator('#close-showInfoError', log_if_not_found=False).is_visible():
            print(f"Invalid Verification Code 팝업 감지됨. OCR 재시도 중... (시도 {attempt + 1}/3)")
            # 팝업 닫기
            # page.locator('#close-showInfoError').click()

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
            print("☑ 카드저장 클릭")
            break  # 팝업이 없으면 루프 종료
    else:
        print("❌ 최대 시도 횟수를 초과했습니다. 카드 추가 실패.")

    # 카드 등록 완료 확인
    page.wait_for_timeout(2000)  # 페이지 업데이트 대기
    page.goto("https://beta-mobile.fashiongo.net/myaccount/mycard") # 다시 한번 카드리스트 이동

    # "VISA ending in 4242" 카드가 있는지 확인
    try:
        card_element = page.locator('p.card-num', has_text="VISA ending in 4242")
        if card_element.is_visible():
            print("🅿 카드 추가 완료 - VISA ending in 4242 확인됨")
            return True
        else:
            print("❌ VISA ending in 4242 카드를 찾을 수 없습니다.")
            pytest.fail("카드 추가 실패: VISA ending in 4242 요소를 찾을 수 없습니다.")
    except Exception as e:
        print(f"❌ 카드 확인 중 오류 발생: {e}")
        pytest.fail(f"카드 확인 실패: {e}")