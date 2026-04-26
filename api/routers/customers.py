from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..models.customers import Customer
from ..schemas import customers as schema

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

# Create customer
@router.post("/", response_model=schema.Customer)
def create_customer(customer: schema.CustomerCreate, db: Session = Depends(get_db)):

    new_customer = Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        address=customer.address
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


# Read all customers
@router.get("/", response_model=list[schema.Customer])
def get_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()


# Read one customer
@router.get("/{customer_id}", response_model=schema.Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):

    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer


# Update customer
@router.put("/{customer_id}", response_model=schema.Customer)
def update_customer(
    customer_id: int,
    updated: schema.CustomerCreate,
    db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer.name = updated.name
    customer.email = updated.email
    customer.phone = updated.phone
    customer.address = updated.address

    db.commit()
    db.refresh(customer)

    return customer


# Delete customer
@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):

    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    db.delete(customer)
    db.commit()

    return {"message": "Customer deleted successfully"}