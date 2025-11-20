from playwright.sync_api import sync_playwright

def launch_browser():
    """
    동기적으로 Playwright 브라우저를 시작합니다.
    
    Returns:
        tuple: (playwright_instance, browser_instance)
            - playwright_instance: Playwright 인스턴스 (브라우저 관리용)
            - browser_instance: 실행된 Chromium 브라우저 인스턴스
    
    Note:
        - headless=False: 브라우저 창을 화면에 표시
        - args=["--kiosk"]: 전체화면 키오스크 모드로 실행
        (브라우저를 전체화면으로 실행하면서 사용자가 브라우저를 종료하거나 다른 애플리케이션으로 전환하기 어렵게 만드는 모드)
    """
    # Playwright 인스턴스 시작 (동기)
    playwright = sync_playwright().start()
    
    # Chromium 브라우저 실행 (키오스크 모드, 화면 표시)
    browser = playwright.chromium.launch(
        headless=False,  # Headless True는 백단에서 실행
        args=[
            # "--kiosk", # 전체화면 키오스크 모드
            "--disable-web-security",  # 보안 제한 해제
            "--disable-features=VizDisplayCompositor" # GPU 렌더링 비활성화
            ]  
    )
    
    return playwright, browser

def close_browser(playwright, browser):
    """
    브라우저와 Playwright 인스턴스를 안전하게 종료합니다.
    
    Args:
        playwright: Playwright 인스턴스
        browser: 브라우저 인스턴스
    
    Note:
        종료 순서가 중요합니다: 브라우저 먼저, 그 다음 Playwright 인스턴스
    """
    # 브라우저 종료 (모든 페이지와 컨텍스트도 함께 정리됨)
    browser.close()
    
    # Playwright 인스턴스 종료 (리소스 정리)
    playwright.stop()