from core.page_wrapper import HighlightPageWrapper

# Group Manager 권한주기
def wa_groupManager(page, logs=None):
   # logs = logs or [] # logs가 None이면 빈 리스트로 초기화
   if logs is None:
      logs = []

   # Group Manager 검색
   logs.append("group manager 메뉴 클릭")
   page.locator('.sidemenu__category__heading .sidemenu__category__heading__name', has_text='Administration').click() # Administration 메뉴 클릭
   page.locator('.sidemenu__category__body__name', has_text='Group Manager').click() # Group Manager 메뉴
   page.wait_for_timeout(3000) # 3초 대기   

   logs.append("[NEW] QA 그룹 검색")
   page.locator('.input-txt.input-md.ng-untouched.ng-pristine.ng-valid').click() # Group inputbox 클릭
   page.locator('.input-txt.input-md.ng-untouched.ng-pristine.ng-valid').type("[new] qa") # inputbox 입력
   page.locator('button.btn.btn-sm.btn-blue.search-box-btn__right').click() # Search 버튼 클릭
   page.locator('.link-blue', has_text='[NEW] QA').click() # Search 버튼 클릭

   # Group Permission 권한주기
   logs.append("Group Permission 권한주기")
   page.locator('button.btn.btn-sm.btn-blue').click() # Edit 버튼 클릭
   page.wait_for_timeout(3000) # 3초 대기   

   # Check all checkboxes
   checkboxes = page.locator('.blue-checkbox')
   count = checkboxes.count()
   print(f"Checkbox count: {count}")  # 체크박스 개수 출력

   for i in range(count):
      checkbox = checkboxes.nth(i)
      input_el = checkbox.locator('input[type="checkbox"]')
      if not input_el.is_checked():
         checkbox.locator('.check-circle').click()  # 실제 클릭은 이 요소에서

   # Save 버튼 클릭
   page.locator('button.btn.btn-md.btn-blue', has_text="Save").click()
   # 저장 팝업
   page.locator('button.k-button.k-primary', has_text="Yes").click() 
   page.wait_for_timeout(5000) # 5초 대기
   logs.append("New QA 그룹 권한 부여 및 저장 완료") # 저장 완료
   print("New QA 그룹 권한 부여 완료") # Group Manager 권한 부여 완료
  
