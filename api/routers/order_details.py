from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal

from ..dependencies.database import get_db
from ..models.order_details import OrderDetail
from ..models.orders import Order
from ..models.menu_items import MenuItem
from ..models.resources import Resource
from ..models.menu_item_resources import MenuItemResource
from ..schemas import order_details as schema


router = APIRouter(
    prefix="/orderdetails",
    tags=["Order Details"]
)

#add item to order
@router.post("/", response_model=schema.OrderDetail)
def add_item_to_order(request: schema.OrderDetailCreate, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == request.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    item = db.query(MenuItem).filter(MenuItem.id == request.menu_item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    qty = request.quantity

    #check ingredients / stock
    ingredients = db.query(MenuItemResource).filter(
        MenuItemResource.menu_item_id == item.id
    ).all()

    for ing in ingredients:
        resource = db.query(Resource).filter(Resource.id == ing.resource_id).first()

        required = ing.quantity_needed * qty

        if not resource:
            continue

        if resource.amount < required:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough {resource.resource_name}"
            )

    #deduct stock
    for ing in ingredients:
        resource = db.query(Resource).filter(Resource.id == ing.resource_id).first()

        if resource:
            resource.amount -= ing.quantity_needed * qty

    #create order detail
    line_total = Decimal(item.price) * qty

    order_detail = OrderDetail(
        order_id=request.order_id,
        menu_item_id=request.menu_item_id,
        quantity=qty,
        price=item.price
    )

    db.add(order_detail)

    #update order total
    order.total_price = (order.total_price or Decimal(0)) + line_total

    db.commit()
    db.refresh(order_detail)

    return order_detail


#read all order items
@router.get("/", response_model=list[schema.OrderDetail])
def get_order_details(db: Session = Depends(get_db)):
    return db.query(OrderDetail).all()


#get single order item
@router.get("/{detail_id}", response_model=schema.OrderDetail)
def get_order_detail(detail_id: int, db: Session = Depends(get_db)):

    detail = db.query(OrderDetail).filter(OrderDetail.id == detail_id).first()

    if not detail:
        raise HTTPException(status_code=404, detail="Order detail not found")

    return detail


#update order item
@router.put("/{detail_id}", response_model=schema.OrderDetail)
def update_order_detail(
    detail_id: int,
    request: schema.OrderDetailUpdate,
    db: Session = Depends(get_db)
):

    detail = db.query(OrderDetail).filter(OrderDetail.id == detail_id).first()

    if not detail:
        raise HTTPException(status_code=404, detail="Order detail not found")

    if request.amount:
        detail.quantity = request.amount

    if request.menu_item_id:
        detail.menu_item_id = request.menu_item_id

    db.commit()
    db.refresh(detail)

    return detail


#delete order item
@router.delete("/{detail_id}")
def delete_order_detail(detail_id: int, db: Session = Depends(get_db)):

    detail = db.query(OrderDetail).filter(OrderDetail.id == detail_id).first()

    if not detail:
        raise HTTPException(status_code=404, detail="Order detail not found")

    db.delete(detail)
    db.commit()

    return {"message": "Order detail deleted successfully"}