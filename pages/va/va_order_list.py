from playwright.sync_api import Page


def orders_list_sections(page: Page) -> None:
    # 1. 사이드 메뉴에서 'Orders' > 'All Orders' 진입
    print("☑ 'Orders' 메인 메뉴 찾기")
    orders_main = page.locator("div.nav__item__title", has_text="Orders")
    print(f"☑ div.nav__item__title found ({page.locator('div.nav__item__title').count()}개)")
    orders_main.first.wait_for(state="visible", timeout=10000)
    print("🅿 'Orders' 메인 메뉴 표시 확인")

    orders_main.first.click()
    print("☑ 'Orders' 메인 메뉴 클릭 (하위 메뉴 펼치기)")

    print("☑ 'All Orders' 하위 메뉴 찾기")
    all_orders_menu = page.locator("div.nav__group__item__title", has_text="All Orders")
    print(f"☑ div.nav__group__item__title found ({page.locator('div.nav__group__item__title').count()}개)")
    all_orders_menu.first.wait_for(state="visible", timeout=10000)
    print("🅿 'All Orders' 하위 메뉴 표시 확인")

    all_orders_menu.first.click()
    print("☑ 'All Orders' 메뉴 클릭 (All Orders 페이지 이동)")

    page.wait_for_load_state("networkidle")
    current_url = page.url
    print(f"☑ 현재 URL: {current_url}")
    assert "/order/orders" in current_url, f"❌ All Orders 페이지가 아님: {current_url}"

    # 2. 검색 인풋 필드 존재 확인
    print("☑ 검색 입력 필드(input[type='search']) 찾기")
    search_input = page.locator("input[type='search']")
    search_input.first.wait_for(state="visible", timeout=10000)
    search_count = search_input.count()
    print(f"☑ input[type='search'] found ({search_count}개)")
    print("🅿 검색 입력 필드 표시 확인")

    # 3. 섹션별 UI 오더 개수 확인 (DOM 직접 탐색)
    print("☑ 오더 섹션 타이틀 및 오더 개수(UI) 확인 시작")

    sections = [
        {"label": "New Orders", "status_id": 1},
        {"label": "Confirmed Orders", "status_id": 2},
        {"label": "Shipped Orders", "status_id": 3},
        {"label": "Canceled Orders", "status_id": 5},
        {"label": "Backorders", "status_id": 7},
    ]

    for section in sections:
        label = section["label"]

        print(f"\n=== '{label}' 섹션(UI) 체크 시작 ===")
        fg_count = page.locator("fg-order-list").count()
        print(f"☑ fg-order-list found ({fg_count}개)")

        # JS로 해당 섹션 fg-order-list를 찾아 tbody tr 개수 카운트
        result = page.evaluate(
            """
            (label) => {
              const lists = Array.from(document.querySelectorAll('fg-order-list'));
              const res = { exists: false, count: 0 };

              for (const list of lists) {
                const header = list.querySelector('.panel__header__title');
                if (!header) continue;

                const text = (header.textContent || '').trim();
                if (!text.includes(label)) continue;

                res.exists = true;

                let total = 0;
                const tbodies = list.querySelectorAll('tbody');
                tbodies.forEach(tbody => {
                  total += tbody.querySelectorAll('tr').length;
                });

                res.count = total;
                break; // 첫 매칭 섹션만 사용
              }

              return res;
            }
            """,
            label,
        )

        if result.get("exists"):
            print(f"🅿 '{label}' 섹션 타이틀 노출 확인")
        else:
            print(f"🅿 '{label}' 섹션 타이틀 DOM 미존재 (헤더 미노출 또는 섹션 숨김 상태일 수 있음)")

        ui_count = int(result.get("count") or 0)
        print(f"🅿 '{label}' 섹션 오더 개수(UI): {ui_count}개")