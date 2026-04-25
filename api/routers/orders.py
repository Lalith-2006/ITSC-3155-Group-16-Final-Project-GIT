from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import random
from datetime import datetime

from ..dependencies.database import get_db
from ..models.orders import Order
from ..models.order_details import OrderDetail
from ..models.menu_items import MenuItem
from ..models.customers import Customer

from ..schemas import orders as schema

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

#Registered User order
@router.post("/", response_model=schema.Order)
def create_order(customer_id: int, items: list[int], db: Session = Depends(get_db)):

    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    order = Order(
        customer_id=customer_id,
        status="pending",
        tracking_number=str(random.randint(100000, 999999)),
        total_price=0
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    total = 0

    for item_id in items:
        item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
        if not item:
            continue

        detail = OrderDetail(
            order_id=order.id,
            menu_item_id=item.id,
            amount=1
        )

        total += float(item.price)
        db.add(detail)

    order.total_price = total
    db.commit()

    return order


#Guest order
@router.post("/guest", response_model=schema.Order)
def guest_order(name: str, email: str, items: list[int], db: Session = Depends(get_db)):

    customer = Customer(name=name, email=email)
    db.add(customer)
    db.commit()
    db.refresh(customer)

    return create_order(customer.id, items, db)



@router.get("/", response_model=list[schema.Order])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()



@router.get("/{order_id}", response_model=schema.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order