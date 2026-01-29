"""
Pydantic schemas for the stateless cart.


These schemas define the contract only.
No database access, no business logic.
"""


import uuid
from decimal import Decimal
from pydantic import BaseModel, PositiveInt




# ---------- Request Schemas ----------


class CartItemIn(BaseModel):
    product_id: uuid.UUID
    quantity: PositiveInt 




class CartRequest(BaseModel):
    items: list[CartItemIn]




# ---------- Response Schemas ----------


class CartItemOut(BaseModel):
    product_id: uuid.UUID
    name: str
    unit_price: Decimal
    quantity: int
    line_total: Decimal



class CartResponse(BaseModel):
    items: list[CartItemOut]
    total: Decimal