from playwright.sync_api import Page
import time

def check_itemlist(page: Page, url: str, min_count: int = 5, timeout: int = 10000):
    """
    주어진 URL에서 상품 리스트가 최소 min_count 이상 렌더링될 때까지 기다리고 확인합니다.
    """
    print(f"\n페이지 이동: {url}")
    page.goto(url, wait_until="domcontentloaded")

    # 최소 하나라도 나타날 때까지 먼저 대기
    page.wait_for_selector("ul.lst_pdt li", timeout=timeout, state="attached")

    # min_count 이상이 될 때까지 polling
    start_time = time.time()
    max_time = timeout / 1000  # ms → 초 단위 변환

    while True:
        count = page.locator("ul.lst_pdt li").count()
        if count >= min_count:
            print(f"상품 {count}개 로딩됨 (최소 기대치 {min_count} 이상)")
            break
        if time.time() - start_time > max_time:
            page.screenshot(path="itemlist_timeout.png", full_page=True)
            raise AssertionError(f"상품이 {min_count}개 이상 로딩되지 않음 (현재 {count}개)")
        time.sleep(0.3)

    print("상품 리스트 정상 노출 확인 완료\n")