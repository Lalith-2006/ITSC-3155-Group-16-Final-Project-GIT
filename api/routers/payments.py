from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..models.payments import Payment
from ..models.orders import Order
from ..schemas import payments as schema

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)

# Create payment
@router.post("/", response_model=schema.Payment)
def create_payment(request: schema.PaymentCreate, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == request.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    payment = Payment(
        order_id=request.order_id,
        payment_type=request.payment_type,
        transaction_status="completed"
    )

    # optional business logic
    order.status = "paid"

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment


# Read all payments
@router.get("/", response_model=list[schema.Payment])
def get_payments(db: Session = Depends(get_db)):
    return db.query(Payment).all()


# Read payment
@router.get("/{payment_id}", response_model=schema.Payment)
def get_payment(payment_id: int, db: Session = Depends(get_db)):

    payment = db.query(Payment).filter(Payment.id == payment_id).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    return payment


# Update payment
@router.put("/{payment_id}", response_model=schema.Payment)
def update_payment(payment_id: int, request: schema.PaymentCreate, db: Session = Depends(get_db)):

    payment = db.query(Payment).filter(Payment.id == payment_id).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    payment.payment_type = request.payment_type
    payment.transaction_status = request.transaction_status

    db.commit()
    db.refresh(payment)

    return payment


# Delete payment
@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):

    payment = db.query(Payment).filter(Payment.id == payment_id).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    db.delete(payment)
    db.commit()

    return {"message": "Payment deleted successfully"}