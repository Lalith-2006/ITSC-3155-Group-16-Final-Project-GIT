from pydantic import BaseModel
from typing import Optional


class PaymentBase(BaseModel):
    order_id: int
    payment_type: str
    amount: Optional[float] = None
    transaction_status: Optional[str] = "pending"


class PaymentCreate(PaymentBase):
    pass


class Payment(PaymentBase):
    id: int

    class Config:
        from_attributes = True