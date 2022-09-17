from typing import Dict, Any
from pydantic import BaseModel
from builtins import Exception as PyException
from enum import Enum


class Status(str, Enum):
    success = "success"
    failed = "failed"


class Error(BaseModel):
    type: str
    code: int
    message: str | list[dict]


class Success(BaseModel):
    code: int | str
    message: str


class Response(BaseModel):
    """The base ApiResponse model"""

    status: Status = Status.success
    success: Success | Dict[str, Any] | BaseModel | None = None
    error: Error | None = None
    data: Dict[str, Any] | BaseModel | None = None

    def dict(self, *args, **kwargs) -> dict[str, Any]:
        kwargs.pop("exclude_none")
        return super().dict(*args, exclude_none=True, **kwargs)

    class Config:
        use_enum_values = True

        @staticmethod
        def schema_extra(schema) -> None:
            if schema.get("properties")["status"]["default"] == "success":
                schema.get("properties").pop("error")
            if schema.get("properties")["status"]["default"] == "failed":
                schema.get("properties").pop("data")
                schema.get("properties").pop("success")


class Exception(PyException):
    """Exception customized to acts as an ErrorResponse"""

    status_code: int
    error: Error

    def __init__(self, status_code: int, error: Error):
        super().__init__(status_code)
        self.status_code = status_code
        self.error = error


EXPIRED_TOKEN = Error(
    type="auth",
    code=105,
    message="You need to renew the Access token using the refresh token",
)

VALIDATION_ERR = Error(type="validation", code=114, message="")

ELIGIBILITY_ERR = Error(type="eligibility", code=115, message="Not eligible")

INVALID_ACCESS_TOKEN = Error(
    type="token", code=101, message="The Access-Token is not valid"
)

INVALID_TOKEN = Error(
    type="auth",
    code=103,
    message="Invalid token",
)


# FIXME why are we creating classes and not instances
class INVALID_ACCESS_TOKENResponse(Response):
    status: Status = Status.failed
    error: Error = INVALID_ACCESS_TOKEN


class ExpiredTokenResponse(Response):
    status: Status = Status.failed
    error: Error = EXPIRED_TOKEN


class ValidationErrorResponse(Response):
    status: Status = Status.failed
    error: Error = VALIDATION_ERR


class EligibilityErrorResponse(Response):
    status: Status = Status.failed
    error: Error = ELIGIBILITY_ERR


def api_exception(status, json) -> Exception:
    """Generate ApiException from zain-backend failed response"""
    error = Error(
        type="zend",
        code=json.get("error", {}).get("code", 0),
        message=json.get("error", {}).get("message", ""),
    )
    return Exception(status_code=status, error=error)


def api_response(json: dict, klass=None) -> Response:
    """Generate ApiResponse/its inheritors from zain-backend successful response"""
    if klass and not issubclass(klass, Response):
        raise TypeError("klass must be ApiResponse")
    message = json.get("success", {}).get("message") or ""
    code = json.get("success", {}).get("code") or 0
    building_data = {
        "status": json.get("status"),
        "success": Success(message=message, code=code) if json.get("success") else None,
        "data": json.get("data"),
    }

    if klass:
        return klass(**building_data)

    return Response(**building_data)
