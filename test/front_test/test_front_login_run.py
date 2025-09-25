# import asyncio: pytest.ini asyncio_mode = auto 설정해서 주석처리
from core.browser_manager import launch_browser, close_browser
from core.page_wrapper import create_highlighted_page
from pages.web.front.front_login import front_login

# @pytest.mark.asyncio: pytest.ini asyncio_mode = auto 설정해서 주석처리
async def test_front_login():
    """
    front 로그인 수동 테스트 실행
    """
    playwright, browser = await launch_browser()
    page = await create_highlighted_page(browser)

    await page.goto("https://beta-www.fashiongo.net", timeout=90000, wait_until='domcontentloaded')

    await front_login(page, account="fr")

    assert "fashiongo" in page.url.lower()
    print("Beta URL 접속 성공")

    await close_browser(playwright, browser)

