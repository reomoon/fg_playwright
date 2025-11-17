from playwright.sync_api import Page

def close_by_close_buttons(page: Page, rounds: int = 3):
    """
    페이지에 떠 있는 모달/팝업을 '닫기 버튼' 클릭만으로 정리한다.
    - 백드롭 제거, 쿠키 조작, ESC 누르기 같은 건 안 함
    - 너무 오래 기다리지 않게 짧은 timeout만 사용
    """
    close_selectors = [
        ".item-close"
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

def close_by_close_mobile(page: Page, rounds: int = 3):
    """
    모바일용: 24시간 안보이기 팝업이 있으면 먼저 닫고, 
    없으면 일반 닫기 아이콘(.icon_close)도 시도
    """
    for r in range(rounds):
        clicked_any = False

        # 1. 우선 시도 24시간 안보이기 팝업 닫기
        sel = ".link-footer-sub"
        loc = page.locator(sel)
        count = loc.count()
        for i in range(min(count, 5)):
            try:
                el = loc.nth(i)
                el.wait_for(state="visible", timeout=500)
                el.click(timeout=700)
                print(f"☑ 모바일 팝업 24시간 안보이기 클릭: {sel}")
                page.wait_for_timeout(120)
                clicked_any = True
            except Exception:
                continue

        # 2. 없으면 일반 x버튼 닫기 아이콘 시도
        if not clicked_any:
            sel = ".icon_close"
            loc = page.locator(sel)
            count = loc.count()
            for i in range(min(count, 5)):
                try:
                    el = loc.nth(i)
                    el.wait_for(state="visible", timeout=500)
                    el.click(timeout=700)
                    print(f"☑ 모바일 팝업 닫기 클릭: {sel}")
                    page.wait_for_timeout(120)
                    clicked_any = True
                except Exception:
                    continue

        if clicked_any:
            break # 팝업을 닫았으면 반복문 완전히 종료
        else:
            print("🅿 추가로 닫을 팝업/모달 없음")
            break