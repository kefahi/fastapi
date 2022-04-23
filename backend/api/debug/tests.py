import os
import requests_mock
from utils.settings import settings
from pathlib import Path
from .geoip import get_freegeoip
from .ext_api import create_user, get_users, PostUser 

path = os.path.dirname(__file__) + "/mocks/"

@requests_mock.Mocker()
def test(m):
    m.get(settings.freegeoip_api, text=Path(path + './geoip.json').read_text())
    r1 = get_freegeoip()

    m.post(settings.mocked_com_api, text=Path(path + './create_user.json').read_text())
    post_user = PostUser(age=10, isPublic=False, status="working")
    r2 = create_user(post_user)

    m.get(settings.mocked_com_api, text=Path(path + './users.json').read_text())
    r3 = get_users(3)

    return [
            {"get_freegeoip": r1},
            {"create_user": r2},
            {"get_users": r3}
            ]
