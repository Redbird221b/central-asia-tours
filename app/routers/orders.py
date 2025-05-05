from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from models.models import Order
from schemas.schemas import OrderCreate, OrderRead
import database.database as database

router = APIRouter(prefix="/orders")


@router.post("/", response_model=OrderRead)
def create_order(o: OrderCreate, db: Session = Depends(database.get_db)):
    order = Order(**o.dict())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get("/", response_model=List[OrderRead])
def list_orders(db: Session = Depends(database.get_db)):
    return db.query(Order).all()


@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(database.get_db)):
    o = db.query(Order).get(order_id)
    if not o: raise HTTPException(404, "Not found")
    return o
