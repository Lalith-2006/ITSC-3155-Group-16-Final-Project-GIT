from sqlalchemy import Column, Integer, String, ForeignKey
from ..dependencies.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    payment_type = Column(String(50))
    card_number = Column(String(20))
    transaction_status = Column(String(50))