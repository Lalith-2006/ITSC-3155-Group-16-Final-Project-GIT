from pydantic import BaseModel
from typing import Optional, List


class MenuItemResourceCreate(BaseModel):
    resource_id: int
    quantity_needed: int


class MenuItemBase(BaseModel):
    item_name: str
    price: float
    calories: Optional[int] = None
    category: Optional[str] = None


class MenuItemCreate(MenuItemBase):
    ingredients: List[MenuItemResourceCreate]


class MenuItem(MenuItemBase):
    id: int

    class Config:
        from_attributes = True