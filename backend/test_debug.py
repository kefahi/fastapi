import os
from fastapi.testclient import TestClient
from main import app
from api.debug.geoip import get_freegeoip
from api.debug.ext_api import create_user, get_users, PostUser

path = os.path.dirname(__file__) + "/mocks/"

client = TestClient(app)

# @requests_mock.Mocker()
# def test(m):
#     m.get(settings.freegeoip_api, text=Path(path + "./geoip.json").read_text())
#     r1 = get_freegeoip()

#     m.post(settings.mocked_com_api, text=Path(path + "./create_user.json").read_text())
#     post_user = PostUser(age=10, isPublic=False, status="working")
#     r2 = create_user(post_user)

#     m.get(settings.mocked_com_api, text=Path(path + "./users.json").read_text())
#     r3 = get_users(3)

#     return [{"get_freegeoip": r1}, {"create_user": r2}, {"get_users": r3}]


async def test_freegeoip():
    response = await get_freegeoip()
    assert response.get("response", {}).get("code", None) == 200

    response = await create_user(PostUser(age=10, isPublic=False, status="working"))
    assert response.get("response", {}).get("code", None) == 100

    response = await get_users(3)
    assert response.get("response", {}).get("code", None) == 150
