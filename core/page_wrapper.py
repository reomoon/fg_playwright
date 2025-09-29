import asyncio

class HighlightPageWrapper:
    """
    Playwright Page 객체를 래핑하여 locator 호출 시 자동으로 하이라이트 표시
    """
    
    def __init__(self, page):
        self._page = page  # 원래 Playwright의 page 객체를 저장
    
    def locator(self, selector, *args, **kwargs): # 동기 유지
        """
        locator 호출 시 자동으로 하이라이트 표시
        
        Args:
            selector: CSS 선택자 또는 다른 선택자
            *args: 추가 위치 인수
            **kwargs: 추가 키워드 인수
        
        Returns:
            Locator: Playwright locator 객체
        """
        # 먼저 locator 생성
        locator = self._page.locator(selector, *args, **kwargs)
        
        # 백그라운드에서 비동기 실행 (메인 흐름 방해하지 않음)
        self._schedule_highlight(selector) # 동기 호출
        
        return locator
    
    def _schedule_highlight(self, selector): # 동기
        """백그라운드에서 하이라이트 적용"""
        try:
            loop = asyncio.get_event_loop()
            loop.create_task(self._apply_highlight(selector))
        except Exception as e:
            pass  # 에러 발생시 무시

    async def _apply_highlight(self, selector): # 비동기
        """실제 하이라이트 적용"""
        try:
            # element 존재 확인
            count = await self._page.locator(selector).count()
            if count > 0:
                print(f"☑ {selector} found ({count}개)")
            else:
                print(f"❌ {selector} not found")

            await self._page.evaluate(""" 
            (selector) => {
                const element = document.querySelector(selector);
                if (element) {
                    element.style.border = '2px solid red';  // 빨간색 테두리 추가
                    setTimeout(() => {
                        element.style.border = '';  // 일정 시간 후 테두리 제거
                    }, 1000);
                }
            }
            """, selector)

        except Exception as e:
            pass  # 하이라이트 실패해도 무시
    
    def __getattr__(self, name):
        """
        다른 page 메서드들을 원본 page 객체에 위임
        (goto, click, fill 등의 메서드들을 자동으로 전달)
        """
        return getattr(self._page, name)

async def create_highlighted_page(browser):
    """브라우저에서 하이라이트 기능이 있는 페이지 생성"""
    page = await browser.new_page()
    return HighlightPageWrapper(page)