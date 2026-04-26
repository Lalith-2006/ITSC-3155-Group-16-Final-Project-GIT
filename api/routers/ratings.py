from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..models.ratings import Rating
from ..models.customers import Customer
from ..schemas import ratings as schema

router = APIRouter(
    prefix="/ratings",
    tags=["Ratings"]
)


@router.post("/", response_model=schema.Rating)
def create_rating(request: schema.RatingCreate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == request.customer_id).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    rating = Rating(
        customer_id=request.customer_id,
        review_text=request.review_text,
        score=request.score
    )

    db.add(rating)
    db.commit()
    db.refresh(rating)

    return rating


@router.get("/", response_model=list[schema.Rating])
def get_ratings(db: Session = Depends(get_db)):
    return db.query(Rating).all()


@router.get("/{rating_id}", response_model=schema.Rating)
def get_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(Rating.id == rating_id).first()

    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    return rating