from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..models.menu_items import MenuItem
from ..models.resources import Resource
from ..models.menu_item_resources import MenuItemResource
from ..schemas import menu_items as schema

router = APIRouter(
    prefix="/Menu",
    tags=["Menu"]
)

#create menu item
@router.post("/", response_model=schema.MenuItem)
def create_menu_item(request: schema.MenuItemCreate, db: Session = Depends(get_db)):

    # 1. Create menu item
    menu_item = MenuItem(
        item_name=request.item_name,
        price=request.price,
        calories=request.calories,
        category=request.category
    )

    db.add(menu_item)
    db.commit()
    db.refresh(menu_item)

    # 2. Add ingredients (recipe mapping)
    for ing in request.ingredients:

        resource = db.query(Resource).filter(Resource.id == ing.resource_id).first()

        if not resource:
            raise HTTPException(
                status_code=404,
                detail=f"Resource ID {ing.resource_id} not found"
            )

        db.add(MenuItemResource(
            menu_item_id=menu_item.id,
            resource_id=ing.resource_id,
            quantity_needed=ing.quantity_needed
        ))

    db.commit()

    return menu_item


#get all menu items
@router.get("/", response_model=list[schema.MenuItem])
def get_menu_items(db: Session = Depends(get_db)):
    return db.query(MenuItem).all()


#get single menu item
@router.get("/{item_id}", response_model=schema.MenuItem)
def get_menu_item(item_id: int, db: Session = Depends(get_db)):

    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    return item


#update menu item
@router.put("/{item_id}", response_model=schema.MenuItem)
def update_menu_item(item_id: int, request: schema.MenuItemCreate, db: Session = Depends(get_db)):

    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    item.item_name = request.item_name
    item.price = request.price
    item.calories = request.calories
    item.category = request.category

    db.commit()
    db.refresh(item)

    return item


#delete menu item
@router.delete("/{item_id}")
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):

    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    db.delete(item)
    db.commit()

    return {"message": "Menu item deleted successfully"}