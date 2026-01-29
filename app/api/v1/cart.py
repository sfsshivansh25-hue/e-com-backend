"""
Cart API endpoints (stateless).

Thin router:
- Accepts request
- Calls service
- Translates domain errors to HTTP
"""

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.cart import CartRequest, CartResponse
from app.services.cart import CartService

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/price", response_model=CartResponse)
async def price_cart(
    payload: CartRequest,
    db: AsyncSession = Depends(get_db),
):
    service = CartService(db)

    try:
        return await service.price_cart(payload)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

