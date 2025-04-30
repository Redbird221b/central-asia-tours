from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, models, database

router = APIRouter(prefix="/orders")


@router.post("/", response_model=schemas.OrderRead)
def create_order(o: schemas.OrderCreate, db: Session = Depends(database.get_db)):
    order = models.Order(**o.dict())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get("/", response_model=List[schemas.OrderRead])
def list_orders(db: Session = Depends(database.get_db)):
    return db.query(models.Order).all()


@router.get("/{order_id}", response_model=schemas.OrderRead)
def get_order(order_id: int, db: Session = Depends(database.get_db)):
    o = db.query(models.Order).get(order_id)
    if not o: raise HTTPException(404, "Not found")
    return o
