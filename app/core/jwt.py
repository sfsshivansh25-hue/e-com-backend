"""
JWT utilities for authentication.


Design goals:
- Stateless authentication
- Short-lived access tokens
- Explicit verification
"""


from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.core.config import settings


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30




class TokenError(Exception):
    pass




def create_access_token(subject: str, role: str) -> str:
    """
Create a signed JWT access token.


Claims:
- sub: user id
- role: user role
- exp: expiration timestamp
"""
    expire = datetime.now(timezone.utc) + timedelta(
    minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )


    payload = {
    "sub": subject,
    "role": role,
    "exp": expire,
    }


    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)




def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT access token.
    Raises TokenError on failure.
    """
    try:
        payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[ALGORITHM],
        )
        return payload
    except JWTError:
        raise TokenError("Invalid or expired token")