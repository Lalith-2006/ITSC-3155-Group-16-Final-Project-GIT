from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class MenuItemResource(Base):
    __tablename__ = "menu_item_resources"

    id = Column(Integer, primary_key=True, index=True)

    # Links to menu item (dish)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)

    # Links to ingredient/resource
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)

    # How much of the ingredient is needed per 1 menu item
    quantity_needed = Column(Integer, nullable=False)


    menu_item = relationship(
        "MenuItem",
        back_populates="resources"
    )

    resource = relationship(
        "Resource",
        back_populates="menu_items"
    )