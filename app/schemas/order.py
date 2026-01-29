import uuid
from decimal import Decimal
from pydantic import BaseModel


class OrderItemOut(BaseModel):
    product_id: uuid.UUID
    product_name: str
    unit_price: Decimal
    quantity: int
    line_total: Decimal


class OrderOut(BaseModel):
    id: uuid.UUID
    total_amount: Decimal
    status: str
    items: list[OrderItemOut]