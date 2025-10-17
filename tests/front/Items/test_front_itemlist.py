# FR TC_7
from playwright.sync_api import Page
from pages.front.items.fr_ItemList import check_itemlist
from tests.front.login.test_front_login_fixture import front_login_fixture

def test_ItemList(front_login_fixture):
   
    page = front_login_fixture  # 로그인된 상태의 page 객체 사용

    # 1. Women 카테고리
    check_itemlist(page, "https://www.fashiongo.net/Catalog/womens-apparel/activewear#cid=1510")

    # 2. New In 페이지
    check_itemlist(page, "https://www.fashiongo.net/NewArrival/catalog")

    # 3. Text 검색 결과 페이지
    search_keyword = "dress"
    search_url = f"https://www.fashiongo.net/Search?q={search_keyword}"
    check_itemlist(page, search_url)