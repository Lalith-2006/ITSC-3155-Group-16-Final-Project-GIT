from sqlalchemy import Column, Integer, String
from ..dependencies.database import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    number = Column(String(20))
    address = Column(String(200))