import pytest
from pages.va.va_create_items import va_create_items_prepack, va_create_items_openpack
from tests.va.test_va_login_fixture import va_login_fixture

@pytest.mark.parametrize("va_login_fixture", ["va"], indirect=True)  # account 파라미터 설정
async def test_create_items_openpack(va_login_fixture):
    page = va_login_fixture    # 로그인된 페이지 사용
    await page.wait_for_timeout(3000) #3초 대기
    product_openpack_id = await va_create_items_openpack(page)
    # product_id를 파일에 저장
    with open("output/created_product_id.txt", "w") as f:
        f.write(str(product_openpack_id))

@pytest.mark.parametrize("va_login_fixture", ["va"], indirect=True)  # account 파라미터 설정
async def test_create_items_prepack(va_login_fixture):
    page = va_login_fixture    # 로그인된 페이지 사용
    await page.wait_for_timeout(3000) #3초 대기
    product_prepack_id = await va_create_items_prepack(page)  # prepack 추가 생성
    # product_id를 파일에 저장
    with open("output/created_product_id.txt", "w") as f:
        f.write(str(product_prepack_id))

# @pytest.mark.parametrize("login_fixture", ["va"], indirect=True)
# async def test_create_items_prepack1(login_fixture):
#     page = login_fixture    # 로그인된 페이지 사용
#     await va_create_items_prepack1(page)  # prepack 추가 생성
    # 브라우저 닫기 (pytest fixture에서 자동으로 닫기 처리)