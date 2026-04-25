from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..models.menu_items import MenuItem
from ..schemas import menu_items as schema

router = APIRouter(
    prefix="/menu",
    tags=['Menu']
)

@router.get("/", response_model=list[schema.MenuItem])
def get_menu(db: Session = Depends(get_db)):
    return db.query(MenuItem).all()

@router.get("/search", response_model=list[schema.MenuItem])
def search_menu(
    category: str = None,
    max_calories: int = None,
    min_calories: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(MenuItem)

    if category:
        query = query.filter(MenuItem.category == category)

    if max_calories:
        query = query.filter(MenuItem.calories <= max_calories)

    if min_calories:
        query = query.filter(MenuItem.calories >= min_calories)

    return query.all()