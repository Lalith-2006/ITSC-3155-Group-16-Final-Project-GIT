from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from ..dependencies.database import get_db
from ..models.orders import Order
from ..models.customers import Customer
from ..schemas import orders as schema

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

#create customer order
@router.post("/", response_model=schema.Order)
def create_order(
    customer_id: int,
    order_type: str,
    db: Session = Depends(get_db)
):

    valid_types = ["takeout", "delivery"]

    if order_type not in valid_types:
        raise HTTPException(status_code=400, detail="Invalid order type")

    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    order = Order(
        customer_id=customer_id,
        status="pending",
        order_type=order_type,
        tracking_number=str(uuid.uuid4())[:8],
        total_price=0
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return order

# create guest order
@router.post("/guest", response_model=schema.Order)
def create_guest_order(
    order_type: str,
    guest_name: str,
    guest_email: str,
    db: Session = Depends(get_db)
):

    valid_types = ["takeout", "delivery"]

    if order_type not in valid_types:
        raise HTTPException(status_code=400, detail="Invalid order type")

    # create temporary customer record
    customer = Customer(
        name=guest_name,
        email=guest_email
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    # create order using generated customer_id
    order = Order(
        customer_id=customer.id,
        status="pending",
        order_type=order_type,
        tracking_number=str(uuid.uuid4())[:8],
        total_price=0
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return order

#get all orders
@router.get("/", response_model=list[schema.Order])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


#get single order
@router.get("/{order_id}", response_model=schema.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


#update order status
@router.put("/{order_id}", response_model=schema.Order)
def update_order(order_id: int, status: str, db: Session = Depends(get_db)):

    valid_statuses = [
        "pending", "paid", "preparing",
        "ready", "completed", "cancelled"
    ]

    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status
    db.commit()
    db.refresh(order)

    return order


#delete order
@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()

    return {"message": "Order deleted successfully"}