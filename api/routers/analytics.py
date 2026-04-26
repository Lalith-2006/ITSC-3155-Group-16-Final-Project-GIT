from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..models.orders import Order

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/revenue/{target_date}")
def get_revenue_by_date(target_date: date, db: Session = Depends(get_db)):
    revenue = (
        db.query(func.sum(Order.total_price))
        .filter(func.date(Order.order_date) == target_date)
        .scalar()
    )

    return {
        "date": target_date,
        "revenue": float(revenue) if revenue else 0
    }


@router.get("/orders/count/{target_date}")
def get_order_count_by_date(target_date: date, db: Session = Depends(get_db)):
    order_count = (
        db.query(func.count(Order.id))
        .filter(func.date(Order.order_date) == target_date)
        .scalar()
    )

    return {
        "date": target_date,
        "order_count": order_count
    }