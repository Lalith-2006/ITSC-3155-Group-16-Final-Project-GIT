from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(String(200))

    orders = relationship("Order", back_populates="customer")
    ratings = relationship("Rating", back_populates="customer")