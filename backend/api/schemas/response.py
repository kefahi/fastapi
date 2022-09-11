from enum import Enum
from pydantic import BaseModel
import api.schemas.errors as api_errors
from typing import Any, Dict
from builtins import Exception as PyException


class Status(str, Enum):
    success = "success"
    failed = "failed"


class APIResponse(BaseModel):
    status: Status
    error: api_errors.Error | None = None
    data: Dict[str, Any] | BaseModel | None = None


class APIException(PyException):
    status_code: int
    error: api_errors.Error

    def __init__(self, status_code: int, error: api_errors.Error):
        super().__init__(status_code)
        self.status_code = status_code
        self.error = error


class INVALID_ACCESS_TOKENResponse(APIResponse):
    status: Status = Status.failed
    error: api_errors.Error = api_errors.INVALID_ACCESS_TOKEN


class ExpiredTokenResponse(APIResponse):
    status: Status = Status.failed
    error: api_errors.Error = api_errors.EXPIRED_TOKEN


class ValidationErrorResponse(APIResponse):
    status: Status = Status.failed
    error: api_errors.Error = api_errors.VALIDATION_ERR


class EligibilityErrorResponse(APIResponse):
    status: Status = Status.failed
    error: api_errors.Error = api_errors.ELIGIBILITY_ERR
