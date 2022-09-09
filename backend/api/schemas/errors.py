""" Errors used in the API. """

from api.schemas.data import Error

# NOT_AUTHENTICATED = Error(type="auth", code=10, message="Not authenticated")

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
