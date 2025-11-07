import cv2
import os

def perform_easyocr(input_image_path):
    """
    EasyOCR을 사용하여 캡챠 이미지를 처리하고 숫자를 추출하는 함수

    Args:
        input_image_path (str): 캡챠 이미지 경로 (output 폴더 내)

    Returns:
        str: OCR로 추출된 숫자 텍스트
    """
    import easyocr

    # output 폴더 경로 설정
    output_dir = os.path.join(os.getcwd(), "output")
    preprocessed_path = os.path.join(output_dir, "preprocessed.png")
    print("🔍 OCR 인식 중")

    # 이미지 전처리 (이진화, 노이즈 제거 등)
    image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
    cv2.imwrite(preprocessed_path, binary_image)  # output 폴더에 저장

    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(preprocessed_path, detail=0)  # output 폴더에서 읽기
    captcha_text = ''.join(filter(str.isdigit, ''.join(results)))
    print(f"☑ EasyOCR 인식 결과: {captcha_text}")
    return captcha_text


def remove_lines(input_image_path, output_image_path):
    """
    이미지에서 선을 감지하고 제거하는 함수

    Args:
        input_image_path (str): 원본 이미지 경로 (output 폴더 내)
        output_image_path (str): 선 제거 후 저장할 이미지 경로 (output 폴더 내)
    """
    import numpy as np

    # 이미지 로드 (input_image_path는 이미 output 폴더 경로 포함)
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

    # 결과 저장 (output_image_path는 이미 output 폴더 경로 포함)
    cv2.imwrite(output_image_path, binary_image)
    print(f"☑ 선 제거된 이미지 저장 완료: {output_image_path}")

def captcha_capture(page, output_image='captcha.png'):
    import os
    
    """
    captcha 캡처 함수 (동기)
    output 폴더에 이미지 저장
    """
    # output 폴더 생성 (없으면)
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)

    # 저장 경로 지정
    output_path = os.path.join(output_dir, output_image)

    # 캡챠 이미지 로드 대기
    page.wait_for_selector("#card_captcha_img", state="attached", timeout=15000)
    page.wait_for_selector("#card_captcha_img", state="visible", timeout=15000)

    # 캡챠 이미지 스크린샷 캡처
    captcha_element = page.locator("#card_captcha_img")
    captcha_element.screenshot(path=output_path)
    print(f"☑ 캡챠 이미지 캡처 완료: {output_path}")
    
    return output_path  # 저장된 파일 경로 반환

def captcha_mobile_capture(page, output_image='captcha.png'):
    import os
    
    """
    captcha 캡처 함수 (동기)
    output 폴더에 이미지 저장
    """
    # output 폴더 생성 (없으면)
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)

    # 저장 경로 지정
    output_path = os.path.join(output_dir, output_image)

    # 캡챠 이미지 로드 대기
    page.wait_for_selector('img[alt="CAPTCHA Image"]', state="attached", timeout=15000)
    page.wait_for_selector('img[alt="CAPTCHA Image"]', state="visible", timeout=15000)

    # 캡챠 이미지 스크린샷 캡처
    captcha_element = page.locator('img[alt="CAPTCHA Image"]')
    captcha_element.screenshot(path=output_path)
    print(f"☑ 캡챠 이미지 캡처 완료: {output_path}")
    
    return output_path  # 저장된 파일 경로 반환