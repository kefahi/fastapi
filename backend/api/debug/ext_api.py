from utils.async_request import AsyncRequest
from utils.logger import logger
from utils.settings import settings
from utils.template import plain_render
from pydantic import BaseModel
import json


class PostUser(BaseModel):
    status: str
    isPublic: bool
    age: int


#  curl https://mockend.com/kefahi/fastapi/users?limit=3
#  curl -d '{"age": 10, "isPublic": false, "status": "working"}' -H "Content-Type: application/json" https://mockend.com/kefahi/fastapi/users


async def create_user(postuser: PostUser) -> dict:
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
    async with AsyncRequest() as client:
        response = await client.post(
            settings.mocked_com_api, json=json.loads(body), headers = headers
        )  # , headers=headers)

    content = await response.text()
    logger.info(
        "Create user",
        extra={
            "props": {
                "body": body,
                "response": {"code": response.status, "content": content},
            }
        },
    )

    return {"content": content, "response": {"code": 100}}


async def get_users(limit: int) -> dict:
    """Get users from external api"""

    async with AsyncRequest() as client:
        response = await client.get(settings.mocked_com_api + f"?limit={limit}")

    content = await response.json()
    logger.info(
        "GeoIP request",
        extra={
            "props": {
                "request": settings.freegeoip_api,
                "response": {"code": response.status, "content": content},
            }
        },
    )

    return {"content": content, "response": {"code": 150}}
