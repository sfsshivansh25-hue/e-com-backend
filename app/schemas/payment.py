# ==============================
# app/schemas/payment.py
# ==============================
from decimal import Decimal
import uuid
from pydantic import BaseModel


class PaymentCreateIn(BaseModel):
    order_id: uuid.UUID
    amount: Decimal


class PaymentOut(BaseModel):
    id: uuid.UUID
    order_id: uuid.UUID
    amount: Decimal
    status: str
    provider: str

    class Config:
        from_attributes = True

class PaymentFailIn(BaseModel):
    reason: str
    
