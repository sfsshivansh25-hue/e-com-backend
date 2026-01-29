from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import uuid

from app.api.deps import get_current_user
from app.db.session import get_db
from app.db.models.order import Order
from app.schemas.order import OrderOut, OrderItemOut
from app.services.checkout import CheckoutService

router = APIRouter(prefix="/checkout", tags=["Checkout"])


@router.post("/{order_id}", response_model=OrderOut)
async def checkout_order(
    order_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    service = CheckoutService(db)

    try:  # ✅ TRANSACTION HERE
            await service.checkout_order(
                order_id=order_id,
                user_id=user.id,
            )
            await db.commit()
    except PermissionError:
        await db.rollback()
        raise HTTPException(status_code=403, detail="Access denied")
    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


    result = await db.execute(
        select(Order)
        .where(Order.id == order_id)
        .options(selectinload(Order.items))
    )
    order = result.scalar_one()

    return OrderOut(
        id=order.id,
        total_amount=order.total_amount,
        status=order.status,
        items=[
            OrderItemOut(
                product_id=i.product_id,
                product_name=i.product_name,
                unit_price=i.unit_price,
                quantity=i.quantity,
                line_total=i.line_total,
            )
            for i in order.items
        ],
    )


@router.post("/{order_id}/cancel", response_model=OrderOut)
async def cancel_order(
    order_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    service = CheckoutService(db)
    try:
        await service.cancel_order(order_id=order_id, user_id=user.id)
        await db.commit()
    except PermissionError:
        await db.rollback()
        raise HTTPException(status_code=403, detail="Access denied")
    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    result = await db.execute(
        select(Order)
        .where(Order.id == order_id)
        .options(selectinload(Order.items))
    )
    order = result.scalar_one()

    return OrderOut(
        id=order.id,
        total_amount=order.total_amount,
        status=order.status,
        items=[
            OrderItemOut(
                product_id=i.product_id,
                product_name=i.product_name,
                unit_price=i.unit_price,
                quantity=i.quantity,
                line_total=i.line_total,
            )
            for i in order.items
        ],
    )
