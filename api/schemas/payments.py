from pydantic import BaseModel
from typing import Optional


class PaymentBase(BaseModel):
    order_id: int
    payment_type: str
    card_number: Optional[str] = None
    transaction_status: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class Payment(PaymentBase):
    id: int

    class Config:
        from_attributes = True