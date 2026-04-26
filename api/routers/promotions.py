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

@router.post("/", response_model=schema.Promotion)
def create_promotion(promo: schema.PromotionCreate, db: Session = Depends(get_db)):

    new_promo = Promotion(
        code=promo.code,
        discount=promo.discount,
        expiration_date=promo.expiration_date,
        is_active=True
    )

    db.add(new_promo)
    db.commit()
    db.refresh(new_promo)

    return new_promo

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

@router.get("/{promo_id}", response_model=schema.Promotion)
def get_promotion(promo_id: int, db: Session = Depends(get_db)):

    promo = db.query(Promotion).filter(Promotion.id == promo_id).first()

    if not promo:
        raise HTTPException(status_code=404, detail="Promotion not found")

    return promo

@router.put("/{promo_id}", response_model=schema.Promotion)
def update_promotion(
    promo_id: int,
    updated: schema.PromotionCreate,
    db: Session = Depends(get_db)
):

    promo = db.query(Promotion).filter(Promotion.id == promo_id).first()

    if not promo:
        raise HTTPException(status_code=404, detail="Promotion not found")

    promo.code = updated.code
    promo.discount = updated.discount
    promo.expiration_date = updated.expiration_date

    db.commit()
    db.refresh(promo)

    return promo

@router.delete("/{promo_id}")
def delete_promotion(promo_id: int, db: Session = Depends(get_db)):

    promo = db.query(Promotion).filter(Promotion.id == promo_id).first()

    if not promo:
        raise HTTPException(status_code=404, detail="Promotion not found")

    db.delete(promo)
    db.commit()

    return {"message": "Promotion deleted successfully"}


