# import asyncio: pytest.ini asyncio_mode = auto 설정해서 주석처리
from core.browser_manager import launch_browser, close_browser
from core.page_wrapper import create_highlighted_page
from pages.front.login.fr_login import front_login

# @pytest.mark.asyncio: pytest.ini asyncio_mode = auto 설정해서 주석처리
async def test_front_login():
    """
    front 로그인 수동 테스트 실행
    """
    # 1. Playwright 브라우저와 컨텍스트를 비동기로 생성 (await로 실행)
    #    - launch_browser()는 비동기 함수이므로 await로 호출해야 실제 브라우저 객체를 반환받을 수 있음
    #    - playwright: Playwright 엔진 객체
    #    - browser: 브라우저 인스턴스 (크롬 등)
    playwright, browser = await launch_browser()

    # 2. 새 페이지를 생성하고, 하이라이트 기능이 포함된 래퍼로 감싸기
    #    - create_highlighted_page(browser)는 비동기 함수이므로 await로 호출
    #    - browser 인스턴스를 인수로 넘겨서 해당 브라우저에서 새 페이지를 생성
    #    - page: 실제로 조작할 Playwright 페이지 객체
    page = await create_highlighted_page(browser)

    # 3. 테스트할 사이트로 이동 (비동기)
    await page.goto("https://beta-www.fashiongo.net", timeout=90000, wait_until='domcontentloaded')

    # 4. 브라우저 창 크기 설정 (비동기 함수이므로 await 필요)
    await page.set_viewport_size({"width": 1680, "height": 900})

    # 5. 로그인 함수 실행 (비동기)
    await front_login(page, account="fr")

    # 6. 로그인 후 URL이 올바른지 page 내 문자 검증
    assert "www.fashiongo" in page.url.lower()
    print("🅿 Beta Front URL 접속 성공")

    # 7. 브라우저 및 Playwright 엔진 종료 (비동기)
    await close_browser(playwright, browser)