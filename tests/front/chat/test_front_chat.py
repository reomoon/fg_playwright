import pytest
from tests.front.login.test_front_login_fixture import front_login_fixture
from pages.front.chat.fr_chat import fr_chat

def test_front_chat(front_login_fixture):
    page = front_login_fixture    # 로그인된 페이지 사용
    fr_chat(page)    # Chat 실행
    # 브라우저 닫기 (pytest fixture에서 자동으로 닫기 처리)   