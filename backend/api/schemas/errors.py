""" Errors used in the API. """


# NOT_AUTHENTICATED = Error(err_type="auth", code=10, message="Not authenticated")

from backend.api.schemas.response import Error


EXPIRED_TOKEN = Error(
    err_type="auth",
    code=105,
    message="You need to renew the Access token using the refresh token",
)

VALIDATION_ERR = Error(err_type="validation", code=114, message="")

ELIGIBILITY_ERR = Error(err_type="eligibility", code=115, message="Not eligible")

INVALID_ACCESS_TOKEN = Error(
    err_type="token", code=101, message="The Access-Token is not valid"
)

INVALID_TOKEN = Error(
    err_type="auth",
    code=103,
    message="Invalid token",
)
