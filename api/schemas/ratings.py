from pydantic import BaseModel
from typing import Optional


class RatingBase(BaseModel):
    customer_id: int
    review_text: Optional[str] = None
    score: int


class RatingCreate(RatingBase):
    pass


class Rating(RatingBase):
    id: int

    class Config:
        from_attributes = True