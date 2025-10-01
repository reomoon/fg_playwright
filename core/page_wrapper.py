import threading # 새로운 스레드를 생성하고 백그라운드에서 실행하기 위해 추가

class HighlightPageWrapper:
    """
    Playwright Page 객체를 래핑하여 locator 호출 시 자동으로 하이라이트 표시하는 클래스
    
    이 클래스는 원본 Playwright Page 객체를 감싸서, 요소를 찾을 때마다
    해당 요소에 빨간색 테두리를 표시하여 시각적으로 확인할 수 있게 도와줍니다.
    
    주요 기능:
    - locator() 호출 시 자동으로 요소 하이라이트
    - 백그라운드에서 하이라이트 처리 (메인 작업 방해 안함)
    - 원본 page의 모든 메서드 그대로 사용 가능
    """
    
    def __init__(self, page):
        """
        HighlightPageWrapper 초기화
        
        Args:
            page: Playwright의 원본 Page 객체
        """
        self._page = page  # 원래 Playwright의 page 객체를 저장

    def locator(self, selector, *args, **kwargs):
        """
        CSS 선택자로 요소를 찾고 자동으로 하이라이트 표시
        
        Args:
            selector (str): CSS 선택자 (예: "#id", ".class", "button")
            *args: locator()에 전달할 추가 위치 인수
            **kwargs: locator()에 전달할 추가 키워드 인수
        
        Returns:
            Locator: Playwright locator 객체 (클릭, 입력 등 가능)
            
        Example:
            button = page.locator("#login-btn")  # 버튼을 찾고 빨간 테두리 표시
            await button.click()  # 버튼 클릭
        """
        # 먼저 원본 page에서 locator 생성
        locator = self._page.locator(selector, *args, **kwargs)
        
        # 백그라운드에서 하이라이트 적용 (메인 작업 방해 안함)
        self._schedule_highlight(selector)
        
        return locator
    
    def _schedule_highlight(self, selector):
        """
        백그라운드 스레드에서 하이라이트를 적용하도록 예약
        
        메인 스레드는 멈추지 않고 계속 진행되며,
        별도 스레드에서 하이라이트만 처리합니다.
        
        Args:
            selector (str): 하이라이트할 요소의 CSS 선택자
        """
        def run_highlight():
            """백그라운드에서 실행될 하이라이트 함수"""
            try:
                self._apply_highlight(selector)
            except Exception as e:
                # 하이라이트 실패해도 메인 작업에 영향 없도록 무시
                pass
        
        # 새로운 스레드 생성 및 시작
        # daemon=True: 메인 프로그램 종료 시 이 스레드도 자동 종료
        thread = threading.Thread(target=run_highlight, daemon=True)
        thread.start()

    def _apply_highlight(self, selector):
        """
        실제로 웹페이지 요소에 하이라이트(빨간 테두리)를 적용
        
        Args:
            selector (str): 하이라이트할 요소의 CSS 선택자
            
        작동 방식:
        1. 요소가 존재하는지 확인하고 개수 출력
        2. JavaScript로 요소에 빨간 테두리 추가
        3. 1초 후 테두리 자동 제거
        """
        try:
            # 1. 요소 존재 여부 및 개수 확인
            count = self._page.locator(selector).count()
            if count > 0:
                print(f"☑ {selector} found ({count}개)")  # 찾은 요소 개수 출력
            else:
                print(f"❌ {selector} not found")  # 요소를 찾지 못함

            # 2. JavaScript로 실제 하이라이트 적용
            self._page.evaluate(""" 
            (selector) => {
                const element = document.querySelector(selector);
                if (element) {
                    // 빨간색 테두리 추가
                    element.style.border = '2px solid red';  
                    
                    // 1초(1000ms) 후 테두리 제거
                    setTimeout(() => {
                        element.style.border = '';  
                    }, 1000);
                }
            }
            """, selector)

        except Exception as e:
            # 하이라이트 실패해도 테스트에 영향 없도록 무시
            pass
    
    def __getattr__(self, name):
        """
        이 클래스에 없는 메서드들을 원본 page 객체에 자동으로 위임
        
        예를 들어:
        - page.goto() → self._page.goto()
        - page.click() → self._page.click()
        - page.fill() → self._page.fill()
        
        이렇게 해서 원본 Playwright Page의 모든 기능을 그대로 사용할 수 있습니다.
        
        Args:
            name (str): 호출하려는 메서드나 속성 이름
            
        Returns:
            원본 page 객체의 해당 메서드나 속성
        """
        return getattr(self._page, name)

def create_highlighted_page(browser):
    """
    브라우저에서 하이라이트 기능이 있는 새 페이지 생성 (동기식)
    
    Args:
        browser: Playwright Browser 객체
        
    Returns:
        HighlightPageWrapper: 하이라이트 기능이 추가된 페이지 객체
        
    사용 예시:
        from core.browser_manager import launch_browser
        from core.page_wrapper import create_highlighted_page
        
        playwright, browser = launch_browser()
        page = create_highlighted_page(browser)
        
        page.goto("https://example.com")
        button = page.locator("#submit-btn")  # 자동으로 빨간 테두리 표시
        button.click()
    """
    # 브라우저에서 새 페이지 생성 (동기식)
    page = browser.new_page()
    
    # 하이라이트 기능을 추가한 래퍼로 감싸서 반환
    return HighlightPageWrapper(page)