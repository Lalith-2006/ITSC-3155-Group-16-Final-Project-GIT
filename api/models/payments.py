from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))

    payment_type = Column(String(50))  # card / cash

    amount = Column(String(50))

    transaction_status = Column(String(50))  # pending / completed / failed

    order = relationship("Order", back_populates="payment")