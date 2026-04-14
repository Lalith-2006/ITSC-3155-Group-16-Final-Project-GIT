from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PromotionBase(BaseModel):
    code: str
    discount: int
    expiration_date: Optional[datetime] = None


class PromotionCreate(PromotionBase):
    pass


class Promotion(PromotionBase):
    id: int

    class Config:
        from_attributes = True