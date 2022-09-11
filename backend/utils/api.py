from pydantic import BaseModel
from typing import Any, Dict
from builtins import Exception as PyException
from enum import Enum


class Status(str, Enum):
    success = "success"
    failed = "failed"


class Error(BaseModel):
    type: str
    code: int
    message: str | list[dict]


class Response(BaseModel):
    status: Status
    error: Error | None = None
    data: Dict[str, Any] | BaseModel | None = None


class Exception(PyException):
    status_code: int
    error: Error

    def __init__(self, status_code: int, error: Error):
        super().__init__(status_code)
        self.status_code = status_code
        self.error = error
