# FG Auto - Playwright 자동화 테스트 프레임워크

Fashion Go 웹사이트의 자동화 테스트를 위한 Playwright 기반 프레임워크입니다.

## 📋 목차

- [프로젝트 구조](#프로젝트-구조)
- [주요 기능](#주요-기능)
- [설치 및 설정](#설치-및-설정)
- [사용 방법](#사용-방법)
- [설정 파일](#설정-파일)
- [테스트 실행](#테스트-실행)
- [주요 컴포넌트](#주요-컴포넌트)

## 📁 프로젝트 구조

```
fgauto/
├─ core/                          # 핵심 모듈
│  ├─ browser_manager.py          # 브라우저 시작/종료 관리
│  ├─ page_wrapper.py             # 페이지 래퍼 (하이라이트 기능)
│  └─ page_account.py             # 로그인 계정 정보
├─ pages/                         # 페이지별 자동화 로직
│  └─ web/
│     └─ front/
│        └─ front_login.py        # 프론트엔드 로그인 로직
├─ test/                          # 테스트 파일
│  └─ front_test/
│     └─ test_front_login_run.py  # 로그인 테스트
├─ pytest.ini                    # pytest 설정 파일
└─ README.md                      # 프로젝트 문서
```

## 주요 기능

### **하이라이트 기능**
- 웹 요소 선택 시 자동으로 빨간색 테두리 표시
- 1초간 표시 후 자동 제거
- 디버깅 및 시각적 확인에 유용

### **다중 계정 지원**
- Front(`fr`), Mobile('mo'), Vendor Admin(`va`), Web Admin(`wa`) 등 다양한 계정 타입 지원
- 계정별 로그인 정보 자동 관리

### 🚀 **비동기 처리**
- Playwright의 비동기 특성을 활용한 효율적인 테스트
- pytest-asyncio를 통한 비동기 테스트 지원

## 🛠 설치 및 설정

### 1. **필수 패키지 설치**
```bash
pip install playwright pytest pytest-asyncio
playwright install chromium
```

### 2. **계정 정보 설정**
`core/page_account.py` 파일에 로그인 정보를 설정하세요:

```python
LOGIN_CREDENTIALS = {
    "fr_username": "your_french_username",
    "fr_password": "your_french_password",
    "us_username": "your_us_username", 
    "us_password": "your_us_password",
    # 추가 계정...
}
```

## 🎮 사용 방법

### **기본 사용법**

```python
from core.browser_manager import launch_browser, close_browser
from core.page_wrapper import create_highlighted_page
from pages.web.front.front_login import front_login

async def main():
    # 브라우저 시작
    playwright, browser = await launch_browser()
    
    # 하이라이트 기능이 있는 페이지 생성
    page = await create_highlighted_page(browser)
    
    # 웹사이트 접속
    await page.goto("https://beta-www.fashiongo.net")
    
    # 로그인 수행
    await front_login(page, account="fr")
    
    # 브라우저 종료
    await close_browser(playwright, browser)
```

### **다양한 계정으로 로그인**

```python
# Front 계정으로 로그인
await front_login(page, account="fr")

# VA 계정으로 로그인  
await front_login(page, account="va")

# WA 계정으로 로그인
await front_login(page, account="wa")
```

## ⚙️ 설정 파일

### **pytest.ini**
```ini
[pytest]
asyncio_mode = auto
asyncio_default_fixture_loop_scope = function
addopts = -s -v --tb=short
```

### **브라우저 설정 옵션**
```python
# 키오스크 모드 (전체화면)
args=["--kiosk"]

# 성능 최적화
args=[
    "--disable-web-security",
    "--disable-features=VizDisplayCompositor",
    "--no-sandbox"
]
```

## 🧪 테스트 실행

### **단일 테스트 실행**
```bash
python -m pytest test/front_test/test_front_login_run.py
```

### **상세 출력으로 실행**
```bash
python -m pytest test/front_test/test_front_login_run.py -v -s
```

### **모든 테스트 실행**
```bash
python -m pytest
```

## 🔧 주요 컴포넌트

### **1. Browser Manager (`core/browser_manager.py`)**
- **기능**: Playwright 브라우저 시작/종료 관리
- **주요 메서드**:
  - `launch_browser()`: 브라우저 시작
  - `close_browser()`: 브라우저 종료

### **2. Page Wrapper (`core/page_wrapper.py`)**
- **기능**: 페이지 객체에 하이라이트 기능 추가
- **특징**:
  - `locator()` 호출 시 자동 하이라이트
  - 백그라운드에서 비동기 처리
  - 원본 페이지 기능 유지

### **3. Front Login (`pages/web/front/front_login.py`)**
- **기능**: Fashion Go 프론트엔드 로그인 자동화
- **처리 과정**:
  1. 쿠키 동의 버튼 클릭
  2. 로그인 버튼 클릭
  3. 계정 정보 입력
  4. 로그인 완료 대기
  5. 팝업 처리

## 🎯 하이라이트 기능 상세

```python
# 요소 선택 시 자동으로 빨간색 테두리 표시
button = page.locator('button')  # 자동 하이라이트!
await button.click()

# JavaScript로 실행되는 하이라이트 로직
element.style.border = '2px solid red';
setTimeout(() => {
    element.style.border = '';
}, 1000);
```

## 📝 사용 예시

### **완전한 로그인 테스트**
```python
async def test_front_login():
    playwright, browser = await launch_browser()
    page = await create_highlighted_page(browser)

    await page.goto("https://beta-www.fashiongo.net")
    await front_login(page, account="fr")

    assert "fashiongo" in page.url.lower()
    print("✅ 로그인 성공!")

    await close_browser(playwright, browser)
```

## 🐛 문제 해결

### **일반적인 오류들**

1. **`pytest-asyncio` 설치 필요**
   ```bash
   pip install pytest-asyncio
   ```

2. **계정 정보 누락**
   - `core/page_account.py`에서 계정 정보 확인

3. **하이라이트가 보이지 않음**
   - 요소가 존재하는지 확인
   - 브라우저 콘솔 메시지 확인

## 🚀 확장 가능성

- 추가 페이지 자동화 모듈
- 다양한 브라우저 지원 (Firefox, Safari)
- 스크린샷 자동 저장
- 테스트 리포트 생성
- CI/CD 파이프라인 통합

---

**개발자**: Fashion Go 자동화 팀  
**버전**: 1.0.0  
**최종 업데이트**: 2025년 9월  

이 프레임워크는 Fashion Go 웹사이트의 효율적인 자동화 테스트를 위해 설계되었습니다. 🎯