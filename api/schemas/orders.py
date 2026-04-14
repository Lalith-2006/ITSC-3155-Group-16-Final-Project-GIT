from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .order_details import OrderDetail


class OrderBase(BaseModel):
    customer_id: int
    tracking_number: Optional[str] = None
    status: Optional[str] = None
    total_price: Optional[float] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    tracking_number: Optional[str] = None
    status: Optional[str] = None
    total_price: Optional[float] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: List[OrderDetail] = []

    class Config:
        from_attributes = True