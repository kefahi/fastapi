from passlib.context import CryptContext
from hashlib import blake2b
from hmac import compare_digest

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    sha256_crypt__default_rounds=91234,
    ldap_salted_md5__salt_size=16,
)
#! TBD to add the salt
SECRET_KEY = b"pseudorandomly generated server secret key"
AUTH_SIZE = 32


def verify_password(plain_password: str, hashed_password: str) -> bool:
    #! TBD removing chk this in production
    if hashed_password.startswith("$"):
        return pwd_context.verify(plain_password, hashed_password)
    return compare_digest(hash_password(plain_password), hashed_password)
    # return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    h = blake2b(digest_size=AUTH_SIZE, key=SECRET_KEY)
    h.update(bytes(password, "utf-8"))
    return h.hexdigest()
