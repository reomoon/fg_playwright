import os
import time
from core.page_wrapper import create_highlighted_page
from playwright.sync_api import Page

def va_upload_brand_media_image_and_submit(page: Page):
    """
    Brand Media Contents Manager에서
    1) Image 타입 신규 컨텐츠 생성
    2) test_media_image.jpg 업로드
    3) Submit 클릭 후 /api/premium/content/upload 응답 검증
    """

    # 1) Home Editor 메뉴 클릭
    print("☑ Home Editor 메뉴 클릭")
    home_editor_btn = page.locator('div.nav__item__title:has-text("Home Editor")')
    page.wait_for_selector('div.nav__item__title:has-text("Home Editor")', timeout=5000)
    home_editor_btn.click()
    print("🅿 Home Editor 펼침 완료")

    # 2) Brand Media Contents Manager 메뉴 클릭
    print("☑ Brand Media Contents Manager 메뉴 클릭")
    brand_media_menu = page.locator(
        'a[href="#/home-editor/brand-media-contents-manager"]'
    )
    page.wait_for_selector(
        'a[href="#/home-editor/brand-media-contents-manager"]', timeout=5000
    )
    brand_media_menu.click()
    print("🅿 Brand Media Contents Manager 이동 완료")

    # 3) "+ Create a New Content" 버튼 클릭
    print("☑ + Create a New Content 버튼 찾기")
    create_btn = page.locator('a.create-content:has-text("+ Create a New Content")')
    if create_btn.count() == 0:
        create_btn = page.locator("a.create-content")
    assert create_btn.first.is_visible(), "❌ + Create a New Content 버튼이 보이지 않습니다."
    create_btn.first.click()
    print("🅿 Create a New Content 클릭 완료")

    # 4) 드롭다운에서 "Image" 옵션 선택
    print("☑ 타입 선택 드롭다운(select) 찾기")
    media_type_select = page.locator('div.input-select select')
    page.wait_for_selector('div.input-select select', timeout=5000)
    print(f"☑ div.input-select select found ({media_type_select.count()}개)")
    assert media_type_select.count() >= 1, "❌ 타입 선택 select 요소를 찾지 못했습니다."

    print("☑ 드롭다운에서 Image 옵션 선택 시도")
    try:
        media_type_select.first.select_option(label="Image")
    except Exception:
        media_type_select.first.select_option("11")
    print("🅿 Image 타입 선택 완료")

    # 5) Title 인풋에 'test media' 입력
    print("☑ Title 인풋 찾기")
    # Title 라벨이 있는 table-grid만 정확히 타겟팅
    title_row = page.locator(
        'div.table-grid:has(div.table-grid__left.width-150:has-text("Title"))'
    )
    print(f'☑ div.table-grid(Title) found ({title_row.count()}개)')
    assert title_row.count() >= 1, "❌ Title 라벨이 있는 행을 찾지 못했습니다."

    # readonly 인풋(이미지 경로 표시용)을 제외하고 실제 입력칸만 선택
    title_input = title_row.first.locator('input[type="text"]:not([readonly])')
    print(f"☑ Title input[type='text']:not([readonly]) found ({title_input.count()}개)")
    assert title_input.count() == 1, "❌ Title 입력 인풋을 정확히 1개 찾지 못했습니다."

    print('☑ Title 인풋에 "test media" 입력')
    title_input.fill("test media")
    print("🅿 Title 입력 완료")

    # 6) 파일 업로드: test_media_image.jpg
    print("☑ 이미지 파일 업로드용 input[type='file'] 찾기")
    file_inputs = page.locator('input[type="file"][accept*="image"]')
    count = file_inputs.count()
    print(f"☑ image file input count = {count}")
    assert count >= 1, "❌ 이미지용 file input 요소를 찾지 못했습니다."
    file_input = file_inputs.first

    print("☑ 테스트용 미디어 이미지 경로 준비")
    project_root = os.getcwd()
    test_img_path = os.path.join(project_root, "image", "test_media_image.jpg")
    print(f"☑ 사용하려는 이미지 경로: {test_img_path}")

    if not os.path.exists(test_img_path):
        raise FileNotFoundError(f"❌ 테스트 이미지 파일이 존재하지 않습니다: {test_img_path}")

    print("☑ 이미지 파일 업로드 시도")
    file_input.set_input_files(test_img_path)
    print("🅿 test_media_image.jpg 업로드 성공")

    # 7) /api/premium/content/upload 응답 감시 핸들러 등록
    print("☑ API 응답 감시 핸들러 등록 (/api/premium/content/upload)")
    captured_responses = []

    def _on_response(res):
        try:
            if (
                "api/premium/content/upload" in res.url
                and res.request.method == "POST"
            ):
                captured_responses.append(res)
                print(f"☑ 캡처된 응답 URL: {res.url}, status={res.status}")
        except Exception as e:
            print(f"❌ response 핸들러에서 예외 발생: {e}")

    page.context.on("response", _on_response)

    # 8) Submit 버튼 클릭
    print("☑ Submit 버튼 찾기")
    submit_btn = page.locator('button:has-text("Submit")')
    assert submit_btn.first.is_visible(), "❌ Submit 버튼을 찾을 수 없습니다."

    print("☑ Submit 버튼 클릭")
    submit_btn.first.click()

    # 9) 응답 대기
    page.wait_for_timeout(5000)

    # 10) 캡처된 응답 검증
    assert captured_responses, "❌ /api/premium/content/upload 응답을 받지 못했습니다."

    response = captured_responses[-1]
    status = response.status
    print(f"☑ 최종 선택된 API 응답 코드: {status}")
    assert status == 200, f"❌ API 응답 실패: {status}"

    # 11) JSON 응답 구조 검증
    try:
        body = response.json()
    except Exception as e:
        raise AssertionError(f"❌ 응답 JSON 파싱 실패: {e}")

    print(f"☑ API 응답 JSON: {body}")

    assert isinstance(body, dict), "❌ 응답 구조가 dict가 아닙니다."
    assert body.get("success") is True, "❌ success 값이 True가 아닙니다."
    assert body.get("data"), "❌ data 값이 비어있거나 False 입니다."

    if body.get("errorCode") is not None:
        print(f"❌ 서버 errorCode: {body.get('errorCode')}, message={body.get('message')}")

    print("🅿 Brand Media Image 업로드 + Submit API 검증 완료")
