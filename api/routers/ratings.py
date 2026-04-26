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

# create rating
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


# get all ratings
@router.get("/", response_model=list[schema.Rating])
def get_ratings(db: Session = Depends(get_db)):
    return db.query(Rating).all()


# get single rating
@router.get("/{rating_id}", response_model=schema.Rating)
def get_rating(rating_id: int, db: Session = Depends(get_db)):

    rating = db.query(Rating).filter(Rating.id == rating_id).first()

    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    return rating


# update rating
@router.put("/{rating_id}", response_model=schema.Rating)
def update_rating(
    rating_id: int,
    request: schema.RatingUpdate,
    db: Session = Depends(get_db)
):

    rating = db.query(Rating).filter(Rating.id == rating_id).first()

    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    if request.customer_id is not None:
        customer = db.query(Customer).filter(Customer.id == request.customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        rating.customer_id = request.customer_id

    if request.review_text is not None:
        rating.review_text = request.review_text

    if request.score is not None:
        rating.score = request.score

    db.commit()
    db.refresh(rating)

    return rating


# delete rating
@router.delete("/{rating_id}")
def delete_rating(rating_id: int, db: Session = Depends(get_db)):

    rating = db.query(Rating).filter(Rating.id == rating_id).first()

    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    db.delete(rating)
    db.commit()

    return {"message": "Rating deleted successfully"}