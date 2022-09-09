from typing import Dict, Any
from pydantic import BaseModel
import api.schemas.errors as api_errors
from .data import Status, Error, Success


# ================================== Response Models
class ApiResponse(BaseModel):
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
        def schema_extra(schema, model) -> None:
            if schema.get("properties")["status"]["default"] == "success":
                schema.get("properties").pop("error")
            if schema.get("properties")["status"]["default"] == "failed":
                schema.get("properties").pop("data")
                schema.get("properties").pop("success")


# ================================== ErrorResponse Models
class ApiException(Exception):
    """Exception customized to acts as an ErrorResponse"""

    status_code: int
    error: Error

    def __init__(self, status_code: int, error: Error):
        super().__init__(status_code)
        self.status_code = status_code
        self.error = error


class INVALID_ACCESS_TOKENResponse(ApiResponse):
    status: Status = Status.failed
    error: Error = api_errors.INVALID_ACCESS_TOKEN


class ExpiredTokenResponse(ApiResponse):
    status: Status = Status.failed
    error: Error = api_errors.EXPIRED_TOKEN


class ValidationErrorResponse(ApiResponse):
    status: Status = Status.failed
    error: Error = api_errors.VALIDATION_ERR


class EligibilityErrorResponse(ApiResponse):
    status: Status = Status.failed
    error: Error = api_errors.ELIGIBILITY_ERR
