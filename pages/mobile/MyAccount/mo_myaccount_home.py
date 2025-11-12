from core.page_wrapper import create_highlighted_page

def mobile_myaccount(page):
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
