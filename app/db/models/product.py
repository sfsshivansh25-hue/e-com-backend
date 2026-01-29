import uuid
from sqlalchemy import String, Text, Boolean, Integer, Numeric, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class Product(Base):
    __tablename__ = "products"


    id: Mapped[uuid.UUID] = mapped_column(
    UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )


    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)


    price: Mapped[float] = mapped_column(
    Numeric(10, 2), nullable=False
    )


    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


    __table_args__ = (
        CheckConstraint("price > 0", name="price_positive"),
        CheckConstraint("stock >= 0", name="stock_non_negative"),
    )