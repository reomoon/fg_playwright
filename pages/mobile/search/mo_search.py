import random
from core.page_wrapper import create_highlighted_page

def mobile_text_search(page):
    # 홈 페이지로 이동
    page.goto('https://beta-mobile.fashiongo.net/home', wait_until="domcontentloaded", timeout=60000)

    # Top Vendor 팝업의 "Don't show again for 24 hours"가 있으면 클릭, 없으면 닫기 버튼 클릭
    dont_show_popup = page.locator('a.link-footer-sub')
    if dont_show_popup.count() > 0 and dont_show_popup.is_visible():
        dont_show_popup.click()
        print("☑ 'Don't show again for 24 hours' 클릭")
    else:
        top_vendor_close = page.locator('button.popup_cover_close')
        if top_vendor_close.count() > 0 and top_vendor_close.is_visible():
            top_vendor_close.click()
            print("☑ Top Vendor 팝업 닫기 클릭")
    
    # 헤더의 Search 입력란을 찾아 클릭하여 포커스
    header_search_input = page.locator('input[placeholder="Search"]')
    header_search_input.click()

    # 검색어 후보 리스트에서 랜덤하게 하나 선택
    random_search = ['diamante jeans', 'floral crop top', 'bodycon dress']
    random_text = random.choice(random_search)  # 랜덤 검색어 선택
    header_search_input.type(random_text, delay=50)  # 검색어 입력 (타이핑 효과)
    
    # 검색 실행 (엔터 입력 또는 검색 버튼 클릭)
    page.keyboard.press("Enter")
    page.wait_for_url("**/search/result;**", timeout=30000)

    # url searchQuery에서 검색어 확인
    import urllib.parse # 문자열(예: 검색어)을 URL에 안전하게 넣을 수 있도록 URL 인코딩(공백 → %20, 한글/특수문자 → %XX 형태) 해주는 함수

    encoded_query = urllib.parse.quote(random_text)
    if f"searchQuery={encoded_query}" in page.url:
        print(f"🅿 Pass: 검색어 '{random_text}'가 URL에 포함되어 있습니다.")
    else:
        print(f"❌ Fail: 검색어 '{random_text}'가 URL에 포함되어 있지 않습니다. ({page.url})")

    page.wait_for_timeout(5000)