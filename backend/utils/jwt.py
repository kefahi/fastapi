import jwt
from time import time
from typing import Any, Dict, Optional
from fastapi import Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.settings import settings
from api.schemas.response import ApiException
import api.schemas.errors as api_errors
import api.schemas.errors as err


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True, fetch_user: bool = False):
        super().__init__(auto_error=auto_error)
        self.fetch_user = fetch_user

    async def __call__(self, request: Request) -> str | Dict[str, Any] | None:
        credentials: Optional[HTTPAuthorizationCredentials] = await super().__call__(
            request
        )
        exception = ApiException(
            status.HTTP_401_UNAUTHORIZED, api_errors.INVALID_ACCESS_TOKEN
        )

        if credentials and credentials.scheme == "Bearer":
            decoded_data = decode_jwt(credentials.credentials)
            if decoded_data.get("grant_type", None):
                raise exception  # Should be access token
            elif decoded_data is None:
                raise exception  # User not found
            else:
                return decoded_data

        raise exception  # No/invalid credentials


def sign_jwt(data: dict, expires=settings.jwt_access_expires) -> str:
    payload = {"data": data, "expires": time() + expires}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
    except:
        raise ApiException(status.HTTP_401_UNAUTHORIZED, error=err.INVALID_TOKEN)
    if "data" not in decoded_token or not decoded_token["data"]:
        raise ApiException(status.HTTP_401_UNAUTHORIZED, error=err.INVALID_TOKEN)
    if decoded_token["expires"] < time():
        raise ApiException(status.HTTP_410_GONE, api_errors.EXPIRED_TOKEN)
    return decoded_token["data"]
