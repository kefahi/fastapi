from utils.async_request import AsyncRequest
from utils.logger import logger
from utils.settings import settings


async def get_freegeoip() -> dict:
    """Retrieve GeoIP details"""

    async with AsyncRequest() as client:
        response = await client.get(settings.freegeoip_api)

    logger.info(
        "GeoIP request",
        extra={
            "props": {
                "request": settings.freegeoip_api,
                "response": {"code": response.status, "content": await response.json()},
            }
        },
    )

    return {"content": response.json(), "response": {"code": 200}}
