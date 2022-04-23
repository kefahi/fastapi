import requests
from utils.logger import logger
from utils.settings import settings
from utils.template import plain_render
from pydantic import BaseModel
import json

class PostUser(BaseModel):
    status: str
    isPublic : bool
    age: int

#  curl https://mockend.com/kefahi/fastapi/users?limit=3 
#  curl -d '{"age": 10, "isPublic": false, "status": "working"}' -H "Content-Type: application/json" https://mockend.com/kefahi/fastapi/users

def create_user(postuser: PostUser) -> dict:
    headers = { "Content-Type": "application/json", }

    body = plain_render(
        __file__,
        "new_user.json.j2",
        {
            "settings": settings,
            "age": postuser.age,
            "public": "true" if postuser.isPublic else "false",
            "status": postuser.status,
        },
    )

    response = requests.post(settings.mocked_com_api, json=json.loads(body)) # , headers=headers)

    logger.info(
        "Create user",
        extra={
            "props": {
                "body": body,
                "response": {
                    "code": response.status_code, 
                    "content": response.text
                },
            }
        },
    )

    return { "content" : response.text, "response": { "code": 100}}


def get_users(limit: int) -> dict:
    """Get users from external api"""
    response = requests.get(settings.mocked_com_api + f"?limit={limit}")

    logger.info(
        "GeoIP request",
        extra={
            "props": {
                "request": settings.freegeoip_api,
                "response": {
                    "code": response.status_code, 
                    "content": response.json()
                },
            }
        },
    )

    return { "content" : response.json(), "response": { "code": 150}}
