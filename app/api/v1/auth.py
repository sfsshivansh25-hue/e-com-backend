from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from app.db.session import get_db
from app.repositories import user
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.services.auth import AuthService
from app.core.jwt import create_access_token


router = APIRouter(prefix="/auth", tags=["Auth"])




@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    try:
        user = await service.register_user(
        email=payload.email,
        password=payload.password,
        )
        return {"id": str(user.id), "email": user.email}
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))




@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    try:
        user = await service.authenticate_user(
        email=payload.email,
        password=payload.password,
    )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_access_token(
        subject=str(user.id),
        role=user.role,
    )
    return TokenResponse(access_token=token)    
