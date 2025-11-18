import os
import time
from core.page_wrapper import create_highlighted_page
from playwright.sync_api import Page

def va_upload_banner_and_submit(page):

    # 1) Home Editor 메뉴 클릭
    print("☑ Home Editor 메뉴 클릭")
    home_editor_btn = page.locator('div.nav__item__title:has-text("Home Editor")')
    page.wait_for_selector('div.nav__item__title:has-text("Home Editor")', timeout=5000)
    home_editor_btn.click()
    print("🅿 Home Editor 펼침 완료")

    # 2) Banner Manager 메뉴 클릭
    print("☑ Banner Manager 메뉴 클릭")
    banner_manager_btn = page.locator('a[href="#/home-editor/banner-manager"]')
    page.wait_for_selector('a[href="#/home-editor/banner-manager"]', timeout=5000)
    banner_manager_btn.click()

    # 2) [중요] Logo* (230 x 54 Pixels) 블록만 선택
    print("☑ Logo 업로드 블록 찾기")
    logo_block = page.locator("fg-banner-manager-input-file").filter(
        has_text="Logo*"
    )
    # 혹시라도 구조가 바뀌었을 때 디버깅용 출력
    count = logo_block.count()
    print(f"☑ Logo 블록 count = {count}")
    assert count == 1, f"❌ Logo 업로드 블록이 {count}개입니다. (1개여야 함)"

    # 3) Logo 블록 안의 file input / Browse 버튼 선택
    print("☑ Logo file input / Browse 버튼 찾기")
    file_input = logo_block.locator('input[type="file"]')
    browse_btn = logo_block.get_by_role("button", name="Browse")

    assert file_input.count() == 1, "❌ Logo file input이 1개가 아님"
    assert browse_btn.is_visible(), "❌ Logo용 Browse 버튼을 찾을 수 없음"
    
    # 4) 테스트용 이미지 준비
    print("☑ 테스트용 이미지 준비")

    # 프로젝트 루트 기준으로 image/test_banner_logo.jpg 사용
    project_root = os.getcwd()
    test_img_path = os.path.join(project_root, "image", "test_banner_logo.jpg")

    print(f"☑ 사용하려는 이미지 경로: {test_img_path}")

    if not os.path.exists(test_img_path):
        raise FileNotFoundError(f"❌ 테스트 이미지 파일이 존재하지 않습니다: {test_img_path}")

    # 5) 파일 업로드
    print("☑ Logo 이미지 업로드 시도")
    file_input.set_input_files(test_img_path)
    print("🅿 Logo 이미지 업로드 성공")

    # 6) Submit 버튼 클릭
    print("☑ Submit 버튼 찾기")
    submit_btn = page.locator('button:has-text("Submit")')
    assert submit_btn.is_visible(), "❌ Submit 버튼 없음"

    # 7) /api/marketing/banners/save 응답을 수집할 리스트 준비
    print("☑ API 응답 감시 핸들러 등록 (/api/marketing/banners/save)")
    captured_responses = []

    def _on_response(res):
        try:
            if (
                "api/marketing/banners/save" in res.url
                and res.request.method == "POST"
            ):
                captured_responses.append(res)
                print(f"☑ 캡처된 응답 URL: {res.url}, status={res.status}")
        except Exception as e:
            print(f"❌ response 핸들러에서 예외 발생: {e}")

    page.context.on("response", _on_response)

    print("☑ Submit 버튼 클릭")
    submit_btn.click()

    # 8) 응답이 들어올 시간을 조금 기다림
    page.wait_for_timeout(5000)  # 5초 정도 대기 (필요하면 조정 가능)

    # 9) 캡처된 응답 검증
    assert captured_responses, "❌ /api/marketing/banners/save 응답을 받지 못했습니다."

    # 가장 최근 응답 하나만 체크
    response = captured_responses[-1]
    status = response.status
    print(f"☑ 최종 선택된 API 응답 코드: {status}")
    assert status == 200, f"❌ API 응답 실패: {status}"

    # JSON 응답 검증
    try:
        body = response.json()
    except Exception as e:
        raise AssertionError(f"❌ 응답 JSON 파싱 실패: {e}")

    print(f"☑ API 응답 JSON: {body}")

    # ✅ 실제 응답은 dict 형태: {'success': True, 'errorCode': None, 'message': 'success', 'data': True}
    assert isinstance(body, dict), "❌ 응답 구조가 dict가 아님"

    # success 플래그 확인
    assert body.get("success") is True, "❌ success 값이 True가 아님"

    # data 필드(True/False)로 저장 성공 여부 확인
    assert body.get("data") is True, "❌ data 값이 True가 아님"

    # (선택) 에러 코드 / 메시지도 참고용으로 출력
    if body.get("errorCode") is not None:
        print(f"❌ 서버 errorCode: {body.get('errorCode')}, message={body.get('message')}")

    print("🅿 Logo 업로드 + Submit API 검증 완료")