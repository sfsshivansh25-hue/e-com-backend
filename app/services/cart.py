# ==============================
# app/services/cart.py (Hardened)
# ==============================
"""
Stateless Cart Service – Hardened

Additional guarantees:
- Duplicate product IDs merged
- Precise error semantics
- Defensive validation
"""

import uuid
from decimal import Decimal
from collections import defaultdict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.product import Product
from app.schemas.cart import CartRequest, CartResponse, CartItemOut


class CartService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def price_cart(self, cart: CartRequest) -> CartResponse:
        if not cart.items:
            return CartResponse(items=[], total=Decimal("0.00"))

        # ---- Merge duplicate product IDs ----
        merged: dict[uuid.UUID, int] = defaultdict(int)
        for item in cart.items:
            merged[item.product_id] += item.quantity

        product_ids = set(merged.keys())

        # ---- Load products ----
        result = await self.session.execute(
            select(Product).where(Product.id.in_(product_ids))
        )
        products = result.scalars().all()

        product_map = {p.id: p for p in products}

        # ---- Missing product ----
        missing = product_ids - product_map.keys()
        if missing:
            raise ValueError("One or more products do not exist")

        priced_items: list[CartItemOut] = []
        total = Decimal("0.00")

        for product_id, quantity in merged.items():
            product = product_map[product_id]

            if not product.is_active:
                raise ValueError(f"Product '{product.name}' is inactive")

            if quantity > product.stock:
                raise ValueError(
                    f"Insufficient stock for product '{product.name}'"
                )

            line_total = product.price * quantity

            priced_items.append(
                CartItemOut(
                    product_id=product.id,
                    name=product.name,
                    unit_price=product.price,
                    quantity=quantity,
                    line_total=line_total,
                )
            )

            total += line_total

        return CartResponse(items=priced_items, total=total)
