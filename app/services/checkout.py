# ==============================
# app/services/checkout.py (extended)
# ==============================
"""
Checkout Service – Failure Handling & Cancellation

Adds:
- Explicit order cancellation
- Safe state transitions
- Inventory release rules
"""

import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models.order import Order
from app.db.models.product import Product
from app.services import order
from app.core.logger import get_logger

logger = get_logger(__name__)



class CheckoutService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def checkout_order(self, *, order_id: uuid.UUID, user_id: uuid.UUID) -> Order:
        result = await self.session.execute(
            select(Order)
            .where(Order.id == order_id)
            .options(selectinload(Order.items))
        )
        order = result.scalar_one_or_none()
        logger.info(
            f"checkout_start order_id={order_id}"
        )

        if not order:
            raise ValueError("Order not found")

        if order.user_id != user_id:
            raise PermissionError("Access denied")

        if order.status != "pending":
            raise ValueError("Only pending orders can be checked out")

        product_ids = [item.product_id for item in order.items]

        result = await self.session.execute(
            select(Product)
            .where(Product.id.in_(product_ids))
            .with_for_update()
        )
        products = result.scalars().all()
        product_map = {p.id: p for p in products}

        for item in order.items:
            product = product_map.get(item.product_id)
            
            logger.info(
                f"inventory_lock product_id={item.product_id} requested_quantity={item.quantity}"
            )
            
            if not product or not product.is_active:
                raise ValueError("Product unavailable during checkout")
            if product.stock < item.quantity:
                raise ValueError(f"Insufficient stock for product '{product.name}'")
            
        for item in order.items:
            product_map[item.product_id].stock -= item.quantity

        order.status = "paid"
        
        logger.info(
            f"checkout_success order_id={order.id} total={order.total_amount}"
            )

        return order


    async def cancel_order(self, *, order_id: uuid.UUID, user_id: uuid.UUID) -> Order:
        """
        Cancel a pending order.
        Paid orders cannot be cancelled here.
        Inventory is NOT released because it was never deducted.
        """
        result = await self.session.execute(
            select(Order)
            .where(Order.id == order_id)
        )
        order = result.scalar_one_or_none()

        if not order:
            raise ValueError("Order not found")

        if order.user_id != user_id:
            raise PermissionError("Access denied")

        if order.status != "pending":
            raise ValueError("Only pending orders can be cancelled")

        order.status = "cancelled"

        return order


