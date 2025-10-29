from playwright.sync_api import Page

def close_by_close_buttons(page: Page, rounds: int = 3):
    """
    페이지에 떠 있는 모달/팝업을 '닫기 버튼' 클릭만으로 정리한다.
    - 백드롭 제거, 쿠키 조작, ESC 누르기 같은 건 안 함
    - 너무 오래 기다리지 않게 짧은 timeout만 사용
    """
    close_selectors = [
        # 텍스트 기반
        "button:has-text('닫기')",
        "button:has-text('Close')",
        "button:has-text('확인')",
        "a:has-text('닫기')",
        "a:has-text('Close')",
        "a:has-text('확인')",
        # aria 라벨/X 버튼들
        "[aria-label='닫기']",
        "[aria-label='Close']",
        ".item-close", ".btn-close", ".close", ".ant-modal-close"
    ]

    for r in range(rounds):
        clicked_any = False
        for sel in close_selectors:
            try:
                loc = page.locator(sel)
                count = loc.count()
                for i in range(min(count, 5)):  # 과도 클릭 방지
                    try:
                        el = loc.nth(i)
                        el.wait_for(state="visible", timeout=500)
                        el.click(timeout=700)
                        print(f"☑ 닫기 클릭: {sel}")
                        page.wait_for_timeout(120)
                        clicked_any = True
                    except Exception:
                        continue
            except Exception:
                continue
        if not clicked_any:
            print("🅿 닫을 팝업/모달 없음")
            break