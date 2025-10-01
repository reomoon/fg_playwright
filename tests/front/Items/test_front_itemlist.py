# FR TC_7
import pytest
from tests.web.FR_tests.test_login import login_fixture
from playwright.sync_api import Page
from Pages.web.FR_Pages.Items.Itemlist import check_itemlist

def test__FR_7_ItemList(login_fixture):
   
    page = login_fixture  # 로그인된 상태의 page 객체 사용

    # 1. Women 카테고리
    check_itemlist(page, "https://beta-www.fashiongo.net/Catalog?cid=12")

    # 2. New In 페이지
    check_itemlist(page, "https://beta-www.fashiongo.net/NewArrival/catalog")

    # 3. Text 검색 결과 페이지
    search_keyword = "dress"
    search_url = f"https://beta-www.fashiongo.net/Search?q={search_keyword}"
    check_itemlist(page, search_url)