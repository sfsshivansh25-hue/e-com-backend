# ==============================
# app/services/payment.py
# ==============================
"""
Payment Service

Responsibilities:
- Create payment intents
- Enforce idempotency
- Authorize payments (simulated)
- Validate order state & amount

Rules:
- Only pending orders can receive payments
- Only one payment per idempotency key per order
- No payment can be authorized if a payment is already captured
"""

from unittest import result
import uuid
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.order import Order
from app.db.models.payment import Payment
from app.schemas import order, payment


class PaymentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_and_authorize_payment(
        self,
        *,
        order_id: uuid.UUID,
        amount: Decimal,
        idempotency_key: str,
        provider: str = "mock",
    ) -> Payment:
        # 1. Load order
        result = await self.session.execute(
            select(Order).where(Order.id == order_id)
        )
        order = result.scalar_one_or_none()

        if not order:
            raise ValueError("Order not found")

        if order.status != "pending":
            raise ValueError("Payments allowed only for pending orders")

        # 2. Check for existing captured payment
        result = await self.session.execute(
            select(Payment).where(
                Payment.order_id == order_id,
                Payment.status == "captured",
            )
        )
        if result.scalar_one_or_none():
            raise ValueError("Order already paid")

        # 3. Idempotency check
        result = await self.session.execute(
            select(Payment).where(
                Payment.order_id == order_id,
                Payment.idempotency_key == idempotency_key,
            )
        )
        existing_payment = result.scalar_one_or_none()
        if existing_payment:
            return existing_payment

        # 4. Amount validation
        if amount != order.total_amount:
            raise ValueError("Payment amount mismatch")

        # 5. Create payment intent
        payment = Payment(
            order_id=order_id,
            amount=amount,
            status="authorized",  # simulated authorization
            provider=provider,
            idempotency_key=idempotency_key,
        )

        self.session.add(payment)
        return payment

    async def capture_payment(
        self,
        *,
        payment_id: uuid.UUID,
    ) -> Payment:
        # 1. Load payment
        result = await self.session.execute(
            select(Payment).where(Payment.id == payment_id)
        )
        payment = result.scalar_one_or_none()

        if not payment:
            raise ValueError("Payment not found")

        if payment.status != "authorized":
            raise ValueError("Only authorized payments can be captured")

        # 2. Load order
        result = await self.session.execute(
            select(Order).where(Order.id == payment.order_id).with_for_update()
        )
        order = result.scalar_one()

        if order.status != "pending":
            raise ValueError("Order is not payable")

        # 3. Ensure no other captured payment exists
        result = await self.session.execute(
            select(Payment).where(
                Payment.order_id == order.id,
                Payment.status == "captured",
            )
        )
        if result.scalar_one_or_none():
            raise ValueError("Order already has a captured payment")

        # 4. Capture payment & finalize order
        payment.status = "captured"
        order.status = "paid"

        return payment
    
    async def refund_payment(self, *, payment_id: uuid.UUID) -> Payment:
        result = await self.session.execute(
            select(Payment).where(Payment.id == payment_id)
        )
        payment = result.scalar_one_or_none()


        if not payment:
            raise ValueError("Payment not found")


        if payment.status != "captured":
            raise ValueError("Only captured payments can be refunded")  

        result = await self.session.execute(
            select(Order).where(Order.id == payment.order_id)
        )
        order = result.scalar_one() 

        payment.status = "refunded"
        order.status = "refunded"


        return payment  

    async def fail_payment(self, *, payment_id: uuid.UUID, reason: str) -> Payment:
            result = await self.session.execute(
                select(Payment).where(Payment.id == payment_id)
            )
            payment = result.scalar_one_or_none()

            if not payment:
                    raise ValueError("Payment not found")


            if payment.status != "authorized":
                raise ValueError("Only authorized payments can fail")

            payment.status = "failed"
            payment.failure_reason = reason
            
            return payment
