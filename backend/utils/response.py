import typing
from starlette.types import Receive, Scope, Send
from utils.logger import logger
from fastapi.responses import JSONResponse
import json


def clean_dict(dict_with_nones):
    if not isinstance(dict_with_nones, dict):
        return dict_with_nones
    result = {}
    for key, value in dict_with_nones.items():
        if value is not None:
            result[key] = clean_dict(value)
    return result


class OurResponse(JSONResponse):
    def __init__(
        self,
        content,
        status_code: int = 200,
        headers=None,
        media_type="application/json",
        background=None,
    ) -> None:
        super().__init__(content, status_code, headers, media_type, background)
        pass

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        await super().__call__(scope, receive, send)
        try:
            extra = scope["state"]["extra"]
            extra["props"]["response"]["body"] = json.loads(self.body)
            if extra.get("props", {}).get("exception", False):
                logger.info("Error", extra=extra)
            else:
                logger.info("Processed", extra=extra)
        except Exception as e:
            logger.info("Error", str(e))

    def render(self, content: typing.Any):
        try:
            data = content if type(content) is dict else json.loads(content)
            return json.dumps(clean_dict(data), indent=2)
        except Exception as e:
            logger.info("Error", str(e))
