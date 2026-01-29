import uuid
from decimal import Decimal
from pydantic import BaseModel, Field 

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    price: Decimal = Field(..., gt=0)
    stock: int = Field(..., ge=0)

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = Field(None, gt=0)
    stock: int | None = Field(None, ge=0)

class ProductOut(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    price: Decimal
    stock: int

    class Config:
        from_attributes = True

