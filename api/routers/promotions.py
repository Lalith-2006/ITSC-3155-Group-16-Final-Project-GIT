from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..models.promotions import Promotion
from ..models.orders import Order
from ..schemas import promotions as schema

router = APIRouter(
    prefix="/promotions",
    tags=["Promotions"]
)



@router.get("/", response_model=list[schema.Promotion])
def get_promotions(db: Session = Depends(get_db)):
    return db.query(Promotion).all()



@router.post("/apply")
def apply_promo(order_id: int, code: str, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    promo = db.query(Promotion).filter(Promotion.code == code).first()
    if not promo:
        raise HTTPException(status_code=404, detail="Invalid promo code")

    discount = float(order.total_price) * (promo.discount / 100)
    order.total_price = float(order.total_price) - discount

    db.commit()

    return {
        "message": "Promo applied",
        "discount": promo.discount,
        "new_total": order.total_price
    }