"""
Order Creation Service

Responsibilities:
- Create an immutable order from a priced cart
- Persist order + items atomically
- Associate order with user

Assumptions:
- Cart is already validated & priced
- No inventory deduction here
"""

import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.order import Order, OrderItem
from app.schemas.cart import CartResponse


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(
        self,
        *,
        user_id: uuid.UUID,
        cart: CartResponse,
    ) -> Order:
        """
        Create an order from a priced cart snapshot.
        This operation is atomic.
        """

        if not cart.items:
            raise ValueError("Cannot create order with empty cart")

        order = Order(
            user_id=user_id,
            total_amount=cart.total,
            status="pending",
        )

        self.session.add(order)
        await self.session.flush()  # ensures order.id exists

        for item in cart.items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                product_name=item.name,
                unit_price=item.unit_price,
                quantity=item.quantity,
                line_total=item.line_total,
            )
            self.session.add(order_item)

        await self.session.commit()
        return order
