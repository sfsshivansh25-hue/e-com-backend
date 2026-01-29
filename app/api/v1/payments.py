# ==============================
# app/api/v1/payments.py
# ==============================
"""
Payment API Endpoints

Endpoints:
- POST /payments            → create & authorize payment
- POST /payments/{id}/capture → capture authorized payment

Rules:
- Requires authentication
- Uses Idempotency-Key header
- Thin API: delegates logic to PaymentService
"""

import uuid
from decimal import Decimal
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.db.models.user import User
from app.schemas.payment import PaymentCreateIn, PaymentOut, PaymentFailIn
from app.services.payment import PaymentService

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("", response_model=PaymentOut, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payload: PaymentCreateIn,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = PaymentService(db)

    try:
        payment = await service.create_and_authorize_payment(
            order_id=payload.order_id,
            amount=payload.amount,
            idempotency_key=idempotency_key,
        )
        await db.commit()
        await db.refresh(payment)
        return payment

    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{payment_id}/capture", response_model=PaymentOut)
async def capture_payment(
    payment_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = PaymentService(db)

    try:
        payment = await service.capture_payment(payment_id=payment_id)
        await db.commit()
        await db.refresh(payment)
        return payment

    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/{payment_id}/refund", response_model=PaymentOut)
async def refund_payment(
    payment_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = PaymentService(db)

    try:
        payment = await service.refund_payment(payment_id=payment_id)
        await db.commit()
        await db.refresh(payment)
        return payment

    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{payment_id}/fail", response_model=PaymentOut)
async def fail_payment(
    payment_id: uuid.UUID,
    payload: PaymentFailIn,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = PaymentService(db)

    try:
        payment = await service.fail_payment(
            payment_id=payment_id,
            reason=payload.reason,
        )
        await db.commit()
        await db.refresh(payment)
        return payment

    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))



