import os
import pytesseract            
from core.page_ocr import captcha_capture, remove_lines, perform_easyocr

# Tesseract-OCR 경로 설정 (윈도우 사용자만 필요)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Pages/front openpack order
def create_card(page):
    """
    My Account > My Cards 이동
    """
    # 자동화 탐지 방지를 위한 HTTP 헤더 추가(goto 전에 설정)
    page.set_extra_http_headers({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    # playwright 내장함수 goto로 이동
    page.goto('https://beta-www.fashiongo.net/MyAccount/CreditCard', timeout=90000)
    print("☑ /MyAccount/CreditCard 이동")

    """
    카드 추가 여부에 따른 if문 실행
    """
    # all_card_cnt 요소의 숫자 가져오기
    try:
        card_count_text = (page.locator("#all_card_cnt").text_content()).strip()
        card_count = int(card_count_text) if card_count_text.isdigit() else 0
        print(f"☑ 감지된 카드 수: {card_count}")
    except Exception as e:
        print(f"❌ 등록된 카드 count 확인 실패: {e}")
        card_count = 0  # 기본값 사용

    # Add New Card 버튼
    page.locator('button.btn.btn_m_blue.cls_add_card.add-new-card-btn.nclick').click()
    # page.wait_for_load_state('networkidle') # 페이지 로딩 상태를 기다림

    # 웹폰트 로딩 대기
    page.evaluate("document.fonts.ready.then(() => console.log('모든 글꼴이 로드됨'))")

    # 카드 정보 입력
    # Stripe 카드번호 입력 필드가 들어 있는 iframe을 선택
    # 'componentName=cardNumber'는 Stripe 내부 iframe URL에서 카드번호 입력용임을 나타냄
    frame = page.frame_locator('iframe[src*="componentName=cardNumber"]')
    # iframe 내부의 input 필드 선택 ('cardnumber'는 Stripe에서 카드 번호 입력에 사용하는 name)
    card_input = frame.locator('input[name="cardnumber"]')

    # 카드번호 입력 확인
    for attempt in range(5): # 3번 반복
        card_input.fill("") # 입력란 초기화
        card_input.fill('4242424242424242')
        entered_value = card_input.input_value() # 입력 값 확인
        
        if entered_value.replace(" ", "") == '4242424242424242': # 띄어쓰기 없애고, 4242 맞는지 확인
            print(f"☑ 카드번호가 정상 입력 되었습니다. ({attempt+1}번 째 시도)")
            break # 끝냄
        else:
            print(f"☒ 카드번호 입력이 잘못 되었습니다. {attempt+1}번 째 시도")
    else:
        print("❌ 카드번호 입력이 실패 하였습니다.")

    page.locator('#card_holder').type('VISA', delay=100)
    card_exp = page.locator('.stripe_exp.inp_txt')
    card_exp.click()
    card_exp.type('0128', delay=100)
    card_secu_code = page.locator('.stripe_secu_code.inp_txt')
    card_secu_code.click()
    card_secu_code.type('123', delay=100)

    # 주소 정보 입력
    # page.locator('#bill_to').click() # BILL TO
    page.locator('#card_addr').type('38 Henry St')
    page.locator('#card_city').type('Brooklyn')
    # 드롭다운에서 "New York" 옵션 선택
    page.locator('#state').select_option('NY')
    page.locator('#card_zipcode').type('11201')
    # page.locator('#country').select_option('United States') # 드롭다운에서 United States" 옵션 선택 value 속성 사용

    # captcha 캡처 함수 불러오기
    captcha_capture(page)

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
        page.locator('.btn.btn_m_blue.add_btn.cls_save_card').click()
        page.wait_for_timeout(3000)  # 3초 대기

        # 팝업 확인(log_if_not_found=False로 실제 팝업이 안나와도 ❌ 출력 안함)
        if page.locator('#close-showInfoError', log_if_not_found=False).is_visible():
            print(f"Invalid Verification Code 팝업 감지됨. OCR 재시도 중... (시도 {attempt + 1}/3)")
            # 팝업 닫기
            page.locator('#close-showInfoError').click()

            # 새로운 캡챠 이미지 캡처
            captcha_capture(page)

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
            page.locator('#card_captcha_answer').fill("")  # 기존 입력값 초기화
            page.locator('#card_captcha_answer').type(captcha_text)
        else:
            print("🅿 카드 추가 완료")
            break  # 팝업이 없으면 루프 종료
    else:
        print("❌ 최대 시도 횟수를 초과했습니다. 카드 추가 실패.")