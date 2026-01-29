
# ==============================
# app/api/v1/orders.py
# ==============================
import uuid
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_current_user , require_admin   
from app.db.session import get_db
from app.db.models.order import Order
from app.schemas.cart import CartRequest
from app.schemas.order import OrderOut, OrderItemOut
from app.services.cart import CartService
from app.services.order import OrderService
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/orders", tags=["Orders"])


from sqlalchemy.orm import selectinload

@router.post("", response_model=OrderOut, status_code=201)
async def create_order(
    cart: CartRequest,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    priced_cart = await CartService(db).price_cart(cart)

    try:
        order = await OrderService(db).create_order(
            user_id=user.id,
            cart=priced_cart,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 🔑 RELOAD ORDER WITH ITEMS
    result = await db.execute(
        select(Order)
        .where(Order.id == order.id)
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


@router.get("/{order_id}", response_model=OrderOut)
async def get_order_by_id(
    order_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    result = await db.execute(
        select(Order)
        .where(Order.id == order_id)
        .options(selectinload(Order.items))
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Ownership check
    if order.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")

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


@router.get("/admin/all", response_model=list[OrderOut], dependencies=[Depends(require_admin)])
async def admin_list_all_orders(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Order).options(selectinload(Order.items))
    )
    orders = result.scalars().unique().all()

    return [
        OrderOut(
            id=o.id,
            total_amount=o.total_amount,
            status=o.status,
            items=[
                OrderItemOut(
                    product_id=i.product_id,
                    product_name=i.product_name,
                    unit_price=i.unit_price,
                    quantity=i.quantity,
                    line_total=i.line_total,
                )
                for i in o.items
            ],
        )
        for o in orders
    ]



