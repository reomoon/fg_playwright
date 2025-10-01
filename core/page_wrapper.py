import threading
import time

class HighlightPageWrapper:
    def __init__(self, page):
        self._page = page

    def locator(self, selector, *args, log_if_not_found=True, **kwargs):
        """
        CSS 선택자로 요소를 찾고 자동으로 하이라이트 표시
        
        Args:
            selector (str): CSS 선택자
            log_if_not_found (bool): 요소를 찾지 못했을 때 로그 출력 여부
        """
        # 먼저 locator 생성
        locator = self._page.locator(selector, *args, **kwargs)
        
        # 동기적으로 하이라이트 + 로깅 처리 (즉시 실행)
        self._apply_highlight_and_log(selector, log_if_not_found)
        
        return locator
    
    def _apply_highlight_and_log(self, selector, log_if_not_found):
        """동기적으로 하이라이트와 로깅을 처리"""
        try:
            # 요소 개수 확인
            count = self._page.locator(selector).count()
            
            if count > 0:
                # 하이라이트 적용 (동기적으로)
                self._apply_highlight(selector)
                print(f"☑ {selector} found ({count}개)")
                
                # log_if_not_found=True가 기본값으로 True일 때만 ❌ 출력
                # log_if_not_found=False로 하면 ❌ 출력 안함
            elif log_if_not_found: 
                print(f"❌ {selector} not found")
                
        except Exception as e:
            if log_if_not_found:
                print(f"❌ {selector} error: {e}")

    def _apply_highlight(self, selector):
        """실제 하이라이트 적용 (동기식)"""
        try:
            self._page.evaluate("""
            (selector) => {
                const elements = document.querySelectorAll(selector);
                elements.forEach(element => {
                    if (element) {
                        element.style.border = '2px solid red';
                        setTimeout(() => {
                            element.style.border = '';
                        }, 1000);
                    }
                });
            }
            """, selector)
        except Exception:
            pass

    def __getattr__(self, name):
        return getattr(self._page, name)

def create_highlighted_page(browser):
    """브라우저에서 하이라이트 기능이 있는 새 페이지 생성"""
    page = browser.new_page()
    return HighlightPageWrapper(page)