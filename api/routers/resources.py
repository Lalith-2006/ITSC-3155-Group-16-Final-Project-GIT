from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..models.resources import Resource
from ..schemas import resources as schema

router = APIRouter(
    prefix="/resources",
    tags=["Resources"]
)

#create
@router.post("/", response_model=schema.Resource)
def create_resource(request: schema.ResourceCreate, db: Session = Depends(get_db)):

    resource = Resource(
        resource_name=request.resource_name,
        amount=request.amount,
        unit=request.unit,
        cost_per_unit=request.cost_per_unit
    )

    db.add(resource)
    db.commit()
    db.refresh(resource)

    return resource


#read all
@router.get("/", response_model=list[schema.Resource])
def get_resources(db: Session = Depends(get_db)):
    return db.query(Resource).all()


#read one
@router.get("/{resource_id}", response_model=schema.Resource)
def get_resource(resource_id: int, db: Session = Depends(get_db)):

    resource = db.query(Resource).filter(Resource.id == resource_id).first()

    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    return resource


#update
@router.put("/{resource_id}", response_model=schema.Resource)
def update_resource(resource_id: int, request: schema.ResourceCreate, db: Session = Depends(get_db)):

    resource = db.query(Resource).filter(Resource.id == resource_id).first()

    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    resource.resource_name = request.resource_name
    resource.amount = request.amount
    resource.unit = request.unit
    resource.cost_per_unit = request.cost_per_unit

    db.commit()
    db.refresh(resource)

    return resource


#delete
@router.delete("/{resource_id}")
def delete_resource(resource_id: int, db: Session = Depends(get_db)):

    resource = db.query(Resource).filter(Resource.id == resource_id).first()

    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    db.delete(resource)
    db.commit()

    return {"message": "Resource deleted successfully"}