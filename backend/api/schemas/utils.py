from .response import ApiException, ApiResponse
from .data import Error, Success


def api_exception(status, json) -> ApiException:
    """Generate ApiException from zain-backend failed response"""
    error = Error(
        type="zend",
        code=json.get("error", {}).get("code", 0),
        message=json.get("error", {}).get("message", ""),
    )
    return ApiException(status_code=status, error=error)


def api_response(json: dict, klass=None) -> ApiResponse:
    """Generate ApiResponse/its inheritors from zain-backend successful response"""
    if klass and not issubclass(klass, ApiResponse):
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

    return ApiResponse(**building_data)
