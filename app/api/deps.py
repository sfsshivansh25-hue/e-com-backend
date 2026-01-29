"""
FastAPI dependencies for authentication & authorization.


Responsibilities:
- Extract Bearer token
- Validate JWT
- Load current user
- Enforce role-based access
"""


import token
import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.jwt import decode_access_token, TokenError
from app.db.models import user
from app.db.session import get_db
from app.repositories.user import UserRepository


#HTTP Bearer scheme to extract token from Authorization header

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
    except TokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    repo = UserRepository(db)
    user = await repo.get_by_id(uuid.UUID(user_id))

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user



async def require_admin(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return user