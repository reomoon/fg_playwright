import pytest
from tests.front.login.test_front_login_fixture import front_login_fixture
from pages.front.search.fr_Text_Search import Text_search

def test_FR_5_TextSearch(front_login_fixture):
    page = front_login_fixture    # 로그인된 페이지 사용
    Text_search(page, "dress")    # 입력한 텍스트로 Text_search 실행
    # 브라우저 닫기 (pytest fixture에서 자동으로 닫기 처리) 