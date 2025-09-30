import cv2

def perform_easyocr(input_image_path):
    """
    * 해당 라이브러리 함수를 사용
    EasyOCR을 사용하여 캡챠 이미지를 처리하고 숫자를 추출하는 함수

    Args:
        input_image_path (str): 캡챠 이미지 경로

    Returns:
        str: OCR로 추출된 숫자 텍스트
    """
    import easyocr

    # 이미지 전처리 (이진화, 노이즈 제거 등)
    image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
    cv2.imwrite("preprocessed.png", binary_image)

    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext("preprocessed.png", detail=0)
    captcha_text = ''.join(filter(str.isdigit, ''.join(results)))
    print(f"EasyOCR 인식 결과: {captcha_text}")
    return captcha_text


def remove_lines(input_image_path, output_image_path):
    """
    이미지에서 선을 감지하고 제거하는 함수

    Args:
        input_image_path (str): 원본 이미지 경로
        output_image_path (str): 선 제거 후 저장할 이미지 경로
    """
    import numpy as np

    # 이미지 로드
    image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)

    # 이진화 (Thresholding)
    _, binary_image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)

    # 가로 선 제거를 위한 커널 생성
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))  # 가로 방향 커널
    detected_lines = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

    # 선 제거
    contours, _ = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        cv2.drawContours(binary_image, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)

    # 결과 저장
    cv2.imwrite(output_image_path, binary_image)
    print(f"선 제거된 이미지 저장 완료: {output_image_path}")

async def captcha_capture(page, ouput_image='captcha.png'):
    """
    captcha 캡처 함수 (비동기)
    """
    # 🔹 캡챠 이미지 로드 대기
    await page.wait_for_selector("#card_captcha_img", state="attached", timeout=15000)
    await page.wait_for_selector("#card_captcha_img", state="visible", timeout=15000)

    # 🔹 캡챠 이미지 스크린샷 캡처
    captcha_element = page.locator("#card_captcha_img")
    await captcha_element.screenshot(path=ouput_image)
    print(f"캡챠 이미지 캡처 완료: {ouput_image}")