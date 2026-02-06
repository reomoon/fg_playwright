from playwright.sync_api import sync_playwright
import os

def launch_browser():
    """
    동기적으로 Playwright 브라우저를 시작합니다.
    
    Returns:
        tuple: (playwright_instance, browser_instance)
    """
    playwright = sync_playwright().start()
    
    headless = os.getenv("HEADLESS", "True").lower() == "true"
    browser = playwright.chromium.launch(
        headless=headless,
        args=[
            "--disable-web-security",
            "--disable-features=VizDisplayCompositor"
        ]
    )
    
    return playwright, browser

def close_browser(playwright, browser):
    """
    브라우저와 Playwright 인스턴스를 안전하게 종료합니다.
    
    Args:
        playwright: Playwright 인스턴스
        browser: 브라우저 인스턴스
    """
    try:
        if browser:
            browser.close()
        if playwright:
            playwright.stop()
    except Exception as e:
        print(f"Error closing browser: {e}")