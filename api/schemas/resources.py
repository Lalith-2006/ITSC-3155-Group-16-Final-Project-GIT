from pydantic import BaseModel
from typing import Optional


class ResourceBase(BaseModel):
    resource_name: str
    amount: int
    unit: str
    cost_per_unit: float


class ResourceCreate(ResourceBase):
    pass


class Resource(ResourceBase):
    id: int

    class Config:
        from_attributes = True