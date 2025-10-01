import pytest
from pages.front.MyAccount.fr_create_card import create_card
from tests.front.login.test_front_login_fixture import front_login_fixture

"""
pytest의 파라미터화 기능을 이용해 동일한 테스트를 여러 계정으로 실행할 수 있게 함
"login_fixture"는 테스트 함수의 매개변수 이름이며, 그 값으로 "mo" (mobile 계정)를 넘김
이 때 indirect=True를 지정하면 "mo"라는 값이 직접 함수에 전달되는 것이 아니라,
pytest가 먼저 login_fixture라는 이름의 fixture에 해당 값을 전달해서 실행하도록 지시함

즉, login_fixture("mo")처럼 작동하여 fixture 내부에서 "mo" 계정 정보를 사용하게 됨
이를 통해 한 테스트 함수를 여러 계정/환경으로 유연하게 테스트 가능함
"""

# "fr" 계정으로 로그인하여 MyCards 기능 테스트
@pytest.mark.parametrize("front_login_fixture", ["fr"], indirect=True)
@pytest.mark.asyncio
async def test_mycard_fr(front_login_fixture):
    page = front_login_fixture  # fixture에서 로그인된 페이지를 받아옴
    await create_card(page)   # 마이카드 기능 실행 (비동기)

# "mo" 계정으로 로그인하여 MyCards 기능 테스트
@pytest.mark.parametrize("front_login_fixture", ["mo"], indirect=True)
@pytest.mark.asyncio
async def test_mycard_mo(front_login_fixture):
    page = front_login_fixture  # fixture에서 로그인된 페이지를 받아옴
    await create_card(page)   # 마이카드 기능 실행 (비동기)