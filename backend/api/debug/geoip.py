import requests
from utils.logger import logger
from utils.settings import settings


def get_freegeoip() -> dict:
    """Retrieve GeoIP details"""
    response = requests.get(settings.freegeoip_api)

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

    return {"content": response.json(), "response": {"code": 200}}
