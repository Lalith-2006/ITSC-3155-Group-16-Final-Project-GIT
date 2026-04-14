from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(100))
    price = Column(DECIMAL)
    calories = Column(Integer)
    category = Column(String(50))

    order_details = relationship("OrderDetail", back_populates="item")