import pytest
from tests.front.login.test_front_login_fixture import front_login_fixture
from pages.front.search.fr_Image_Search import Image_search

def test_fr_ImageSearch(front_login_fixture):
    page = front_login_fixture    # 로그인된 페이지 사용
    Image_search(page)    # Image Serach 실행
    # 브라우저 닫기 (pytest fixture에서 자동으로 닫기 처리) 