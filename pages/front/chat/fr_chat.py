from core.page_wrapper import HighlightPageWrapper
import time

def fr_chat(page):
    context = page.context

    # 채팅 아이콘 클릭하여 채팅 페이지로 이동 > 새창으로 이동하여 추적
    with context.expect_page() as new_page_info:
        page.click("css=.icon-common.chat.nclick")
    chat_page = new_page_info.value

    # 벤더 검색에 bibi 벤더 검색
    search_input = chat_page.locator("input.input-search")
    search_input.wait_for(state="visible", timeout=10000)

    for char in "bibi":
        search_input.type(char)
        chat_page.wait_for_timeout(1500)

    # 결과 늦게 뜰 수 있으니 명시적으로 대기
    chat_page.wait_for_selector(".user-item", state="attached", timeout=15000)

    # 검색 결과에 노출된 bibi 벤더 클릭
    user_items = chat_page.locator(".user-item")
    count = user_items.count()
    print("☑ user-item count:", count)

    found = False
    for i in range(count):
        item = user_items.nth(i)
        print(f"🔍 user-item[{i}] visible?:", item.is_visible())
        print(f"☑ text:", item.inner_text())

        if item.is_visible():
            item.click()
            found = True
            break

    if not found:
        raise Exception("❌ No visible .user-item found to click.")

    # 채팅방에 메시지 입력 후 전송 버튼 클릭
    message = "test chat message"
    chat_page.fill("textarea.input-chat", message)
    chat_page.click("button#btn-send")

    # 메시지 전송 여부 확인
    try:
        chat_page.wait_for_selector(f"text={message}", timeout=5000)
        print("☑ 메시지 전송 성공")
    except:
        print("☑ 메시지 전송 실패 또는 응답 없음")

    # 4. 이미지 파일 전송
    # page.set_input_files("input[type='file']", "C:\Users\NHN\Pictures\item test image/2025-03-18 15 35 14.jpg")
    # time.sleep(2)  # 업로드 처리 시간 대기
    # page.click("button:has-text('send')")  # 이미지 전송



