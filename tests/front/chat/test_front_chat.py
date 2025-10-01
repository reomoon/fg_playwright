import pytest
from test_login import login_fixture
from Pages.web.FR_Pages.Chat.Chat import Chat

def test_FR_4_Chat(login_fixture):
    page = login_fixture    # 로그인된 페이지 사용
    Chat(page)    # Chat 실행
    # 브라우저 닫기 (pytest fixture에서 자동으로 닫기 처리)   