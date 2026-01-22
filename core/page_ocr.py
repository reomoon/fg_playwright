import cv2
import os
from PIL import Image
import numpy as np

def perform_easyocr(input_image_path):
    """
    고속 EasyOCR - 빠른 인식 최우선
    최소한의 전처리로 속도 극대화
    """
    import easyocr
    import torch
    
    print("🔍 EasyOCR 인식 중...")

    # 이미지 로드
    image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"❌ 이미지 로드 실패: {input_image_path}")
        return ""
    
    # 이미지 정보 출력 (디버깅용)
    print(f"📷 이미지 크기: {image.shape}")
    
    # 최소한의 전처리: 간단한 이진화만
    _, binary = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
    
    # EasyOCR 인식 - GPU 사용 가능하면 활용
    try:
        gpu_available = torch.cuda.is_available()
        # 매번 새로운 리더 인스턴스 생성 (캐시 방지)
        reader = easyocr.Reader(['en'], gpu=gpu_available, verbose=False)
        results = reader.readtext(binary, detail=0)
        captcha_text = ''.join(filter(str.isdigit, ''.join(results))).strip()
        
        print(f"☑ EasyOCR 인식 결과: {captcha_text}")
        # 메모리 정리
        del reader
        return captcha_text
    except Exception as e:
        print(f"❌ EasyOCR 오류: {e}")
        return ""


def remove_lines(input_image_path, output_image_path):
    """
    이미지에서 선을 감지하고 제거하는 함수

    Args:
        input_image_path (str): 원본 이미지 경로 (output 폴더 내)
        output_image_path (str): 선 제거 후 저장할 이미지 경로 (output 폴더 내)
    """
    import numpy as np
    import time

    # 이미지 로드 (input_image_path는 이미 output 폴더 경로 포함)
    image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"❌ 이미지 로드 실패: {input_image_path}")
        return

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
    success = cv2.imwrite(output_image_path, binary_image)
    if success:
        time.sleep(0.5)  # 파일 I/O 완료 대기
        print(f"☑ 선 제거된 이미지 저장 완료: {output_image_path}")
    else:
        print(f"❌ 이미지 저장 실패: {output_image_path}")

def captcha_capture(page, output_image='captcha.png'):
    import os
    import hashlib
    import time
    
    """
    captcha 캡처 함수 (동기)
    output 폴더에 이미지 저장
    """
    # output 폴더 생성 (없으면)
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)

    # 저장 경로 지정
    output_path = os.path.join(output_dir, output_image)
    
    # 이전 파일의 해시값 저장 (변경 감지용)
    previous_hash = None
    if os.path.exists(output_path):
        try:
            with open(output_path, 'rb') as f:
                previous_hash = hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            print(f"⚠️ 이전 파일 읽기 오류: {e}")

    # 캡챠 이미지 로드 대기
    page.wait_for_selector("#card_captcha_img", state="attached", timeout=15000)
    page.wait_for_selector("#card_captcha_img", state="visible", timeout=15000)
    page.wait_for_timeout(500)  # 이미지 렌더링 완료 대기

    # 캡챠 새로고침 버튼이 있다면 클릭 (페이지에 따라 다를 수 있음)
    try:
        refresh_btn = page.locator("button[class*='refresh'], a[class*='refresh'], .captcha-refresh", log_if_not_found=False)
        if refresh_btn.is_visible():
            refresh_btn.click()
            page.wait_for_timeout(1000)  # 새로운 캡챠 생성 대기
    except Exception as e:
        pass  # 새로고침 버튼이 없을 수 있음

    # 캡챠 이미지 스크린샷 캡처
    captcha_element = page.locator("#card_captcha_img")
    captcha_element.screenshot(path=output_path)
    
    # 파일이 실제로 새로 쓰여졌는지 검증
    max_retry = 5
    for retry in range(max_retry):
        time.sleep(0.3)  # 파일 시스템 동기화 대기
        try:
            if os.path.exists(output_path):
                with open(output_path, 'rb') as f:
                    current_hash = hashlib.md5(f.read()).hexdigest()
                
                # 이전 파일과 다르면 성공
                if previous_hash is None or current_hash != previous_hash:
                    print(f"☑ 캡챠 이미지 캡처 완료: {output_path} (해시: {current_hash[:8]}...)")
                    return output_path
                else:
                    print(f"⚠️ 파일이 변경되지 않음. 재캡처 중... ({retry + 1}/{max_retry})")
                    # 캡챠 요소 다시 캡처 시도
                    captcha_element.screenshot(path=output_path)
            else:
                print(f"⚠️ 파일이 생성되지 않음. 재시도 중... ({retry + 1}/{max_retry})")
        except Exception as e:
            print(f"⚠️ 파일 검증 오류: {e}")
    
    print(f"❌ 캡챠 이미지 캡처 검증 실패")
    return output_path

def captcha_mobile_capture(page, output_image='captcha.png'):
    import os
    import hashlib
    import time
    
    """
    captcha 캡처 함수 (동기)
    output 폴더에 이미지 저장
    """
    # output 폴더 생성 (없으면)
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)

    # 저장 경로 지정
    output_path = os.path.join(output_dir, output_image)
    
    # 이전 파일의 해시값 저장 (변경 감지용)
    previous_hash = None
    if os.path.exists(output_path):
        try:
            with open(output_path, 'rb') as f:
                previous_hash = hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            print(f"⚠️ 이전 파일 읽기 오류: {e}")

    # 캡챠 이미지 로드 대기
    page.wait_for_selector('img[alt="CAPTCHA Image"]', state="attached", timeout=15000)
    page.wait_for_selector('img[alt="CAPTCHA Image"]', state="visible", timeout=15000)
    page.wait_for_timeout(500)  # 이미지 렌더링 완료 대기

    # 캡챠 새로고침 버튼이 있다면 클릭 (페이지에 따라 다를 수 있음)
    try:
        refresh_btn = page.locator("button[class*='refresh'], a[class*='refresh'], .captcha-refresh", log_if_not_found=False)
        if refresh_btn.is_visible():
            refresh_btn.click()
            page.wait_for_timeout(1000)  # 새로운 캡챠 생성 대기
    except Exception as e:
        pass  # 새로고침 버튼이 없을 수 있음

    # 캡챠 이미지 스크린샷 캡처
    captcha_element = page.locator('img[alt="CAPTCHA Image"]')
    captcha_element.screenshot(path=output_path)
    
    # 파일이 실제로 새로 쓰여졌는지 검증
    max_retry = 5
    for retry in range(max_retry):
        time.sleep(0.3)  # 파일 시스템 동기화 대기
        try:
            if os.path.exists(output_path):
                with open(output_path, 'rb') as f:
                    current_hash = hashlib.md5(f.read()).hexdigest()
                
                # 이전 파일과 다르면 성공
                if previous_hash is None or current_hash != previous_hash:
                    print(f"☑ 캡챠 이미지 캡처 완료: {output_path} (해시: {current_hash[:8]}...)")
                    return output_path
                else:
                    print(f"⚠️ 파일이 변경되지 않음. 재캡처 중... ({retry + 1}/{max_retry})")
                    # 캡챠 요소 다시 캡처 시도
                    captcha_element.screenshot(path=output_path)
                if previous_hash is None or current_hash != previous_hash:
                    print(f"☑ 캡챠 이미지 캡처 완료: {output_path} (해시: {current_hash[:8]}...)")
                    return output_path
                else:
                    print(f"⚠️ 파일이 변경되지 않음. 재시도 중... ({retry + 1}/{max_retry})")
            else:
                print(f"⚠️ 파일이 생성되지 않음. 재시도 중... ({retry + 1}/{max_retry})")
        except Exception as e:
            print(f"⚠️ 파일 검증 오류: {e}")
    
    print(f"❌ 캡챠 이미지 캡처 검증 실패")
    return output_path