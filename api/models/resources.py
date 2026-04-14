from sqlalchemy import Column, Integer, String, DECIMAL
from ..dependencies.database import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    resource_name = Column(String(100))
    amount = Column(Integer)
    unit = Column(String(20))
    cost_per_unit = Column(DECIMAL)