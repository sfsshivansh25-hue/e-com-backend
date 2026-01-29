# ==============================
# app/db/models/payment.py
# ==============================
import uuid
from sqlalchemy import Column, String, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)

    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False, default="created")

    provider = Column(String(50), nullable=False, default="mock")
    idempotency_key = Column(String(100), nullable=False)
    failure_reason = Column(String(255), nullable=True)

    order = relationship("Order", back_populates="payments")





