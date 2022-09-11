#!/usr/bin/env -S BACKEND_ENV=secrets.env python3
""" FastApi Main module """

import asyncio
import json
import sys
import time
import traceback
from datetime import datetime
from os.path import exists
from typing import Any
import json_logging
from fastapi import Depends, FastAPI, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from hypercorn.asyncio import serve
from hypercorn.config import Config
from starlette.exceptions import HTTPException as StarletteHTTPException
from api.schemas import examples as api_examples
from api.schemas.response import APIException, APIResponse, Status
from api.schemas.errors import Error
from utils.response import OurResponse
from utils.logger import logger
from utils.settings import settings

json_logging.init_fastapi(enable_json=True)

app = FastAPI(
    title="FAST API SKELETON",
    description="""### API microservice for blank project
#### Notes:

* APIs with the 🔒 'lock' icon, require the http header `Authorization: Bearer ABC`.
* Invoke the login api and use the returned access token in the Authorization form button in the upper right section of this documentation.
* All the api responses are in application/json format.
* All apis also return X-Server-Time as  http header response, the value of which is iso-formatted server timestamp.
    """,
    default_response_class=OurResponse,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    openapi_tags=[],
    version="0.0.1",
    redoc_url=None,
)

json_logging.init_request_instrument(app)


service_start_time: str = ""


@app.on_event("startup")
async def app_startup():
    logger.info("Starting")
    global service_start_time
    service_start_time = datetime.now().isoformat()

    openapi_schema = app.openapi()
    """ Example for altering an endpoint
    paths = openapi_schema["paths"]
    for path in paths:
        if path in ["/api/user/logout", "/api/user/delete"]:
            for method in paths[path]:
                responses = paths[path][method]["responses"]
                if responses.get("422"):
                    responses.pop("422")
    """
    app.openapi_schema = openapi_schema


@app.on_event("shutdown")
async def app_shutdown():
    logger.info("Application shutdown")


async def capture_body(request: Request):
    request.state.request_body = {}
    if (
        request.method == "POST"
        and request.headers.get("content-type") == "application/json"
    ):
        request.state.request_body = await request.json()


@app.exception_handler(StarletteHTTPException)
async def my_exception_handler(_, exception):
    return OurResponse(content=exception.detail, status_code=exception.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError):
    err = jsonable_encoder({"detail": exc.errors()})["detail"]
    raise APIException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error=Error(code=422, err_type="validation", message=err),
    )


@app.middleware("http")
async def middle(request: Request, call_next):
    """Wrapper function to manage errors and logging"""
    if request.url._url.endswith("/docs") or request.url._url.endswith("/openapi.json"):
        return await call_next(request)

    start_time = time.time()
    response_body: str = ""
    exception_data: dict[str, Any] | None = None

    # The api_key is enforced only if it set to none-empty value
    if not settings.api_key or (
        "key" in request.query_params
        and settings.api_key == request.query_params["key"]
    ):
        try:
            response = await call_next(request)
        except APIException as ex:
            response = JSONResponse(
                status_code=ex.status_code,
                content=jsonable_encoder(
                    APIResponse(status=Status.failed, error=ex.error)
                ),
            )
            stack = [
                {
                    "file": frame.f_code.co_filename,
                    "function": frame.f_code.co_name,
                    "line": lineno,
                }
                for frame, lineno in traceback.walk_tb(ex.__traceback__)
                if "site-packages" not in frame.f_code.co_filename
            ]
            exception_data = {"props": {"exception": str(ex), "stack": stack}}
            response_body = json.loads(response.body.decode())

        except Exception:
            if ex := sys.exc_info()[1]:
                stack = [
                    {
                        "file": frame.f_code.co_filename,
                        "function": frame.f_code.co_name,
                        "line": lineno,
                    }
                    for frame, lineno in traceback.walk_tb(ex.__traceback__)
                    if "site-packages" not in frame.f_code.co_filename
                ]

                exception_data = {"props": {"exception": str(ex), "stack": stack}}
            response = JSONResponse(
                status_code=500,
                content={
                    "status": "failed",
                    "error": {"code": 99, "message": "internal error"},
                },
            )
            response_body = json.loads(response.body.decode())
    else:
        response = JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(
                APIResponse(
                    status=Status.failed,
                    error=Error(
                        err_type="bad request", code=112, message="Invalid request."
                    ),
                )
            ),
        )
        response_body = json.loads(response.body.decode())

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers["X-Server-Time"] = datetime.now().isoformat()

    extra = {
        "props": {
            "duration": 1000 * (time.time() - start_time),
            "request": {
                "verb": request.method,
                "path": str(request.url.path),
                "headers": dict(request.headers.items()),
                "query_params": dict(request.query_params.items()),
                "body": request.state.request_body
                if hasattr(request.state, "request_body")
                else {},
            },
            "response": {
                "headers": dict(response.headers.items()),
                "body": response_body,
            },
            "http_status": response.status_code,
        }
    }

    if exception_data is not None:
        extra["props"]["exception"] = exception_data
    if hasattr(request.state, "request_body"):
        extra["props"]["request"]["body"] = request.state.request_body
    if response_body:
        extra["props"]["response"]["body"] = response_body

    request.state.extra = extra
    return response


@app.get("/", include_in_schema=False, dependencies=[Depends(capture_body)])
async def root():
    """Micro-service card identifier"""

    version: str = "unknown"
    try:
        if exists("version.txt"):
            with open("version.txt", "r") as version_file:
                version = version_file.read().strip()
    except Exception:
        pass

    return {
        "name": "GMW",
        "type": "microservice",
        "description": "Galleon Middleware for Self-service",
        "status": "success",
        "start_time": service_start_time,
        "current_time": datetime.now(),
        "version": version,
        "server": settings.servername,
    }


""" Including Routes example
app.include_router(
    user,
    prefix="/api/user",
    dependencies=[Depends(capture_body)],
    tags=["user"],
    responses=api_examples.general_response([api_examples.validation]),
)
"""


@app.options("/{x:path}", include_in_schema=False)
async def myoptions():
    return Response(status_code=status.HTTP_200_OK)


@app.get("/{x:path}", include_in_schema=False, dependencies=[Depends(capture_body)])
@app.post("/{x:path}", include_in_schema=False, dependencies=[Depends(capture_body)])
@app.put("/{x:path}", include_in_schema=False, dependencies=[Depends(capture_body)])
@app.patch("/{x:path}", include_in_schema=False, dependencies=[Depends(capture_body)])
@app.delete("/{x:path}", include_in_schema=False, dependencies=[Depends(capture_body)])
async def catchall():
    raise APIException(
        status_code=status.HTTP_404_NOT_FOUND,
        error=Error(
            err_type="catchall", code=501, message="Requested method or path is invalid"
        ),
    )


if __name__ == "__main__":
    config = Config()
    config.bind = [f"{settings.listening_host}:{settings.listening_port}"]
    # config.loglevel = "ERROR"
    # config.logger_class = logging.StreamHandler
    config.accesslog = logger
    config.errorlog = logger
    config.logconfig = "./json_log.ini"

    asyncio.run(serve(app, config))  # type: ignore
