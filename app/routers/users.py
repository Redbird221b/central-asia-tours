from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from models.models import User
import schemas.schemas as schemas
import database.database as database
router = APIRouter(prefix="/users")


@router.post("/", response_model=schemas.UserRead)
def create_user(u: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user = User(
        username=u.username,
        hashed_password=auth.get_password_hash(u.password),
        access=u.access
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/", response_model=List[schemas.UserRead])
def list_users(db: Session = Depends(database.get_db)):
    return db.query(User).all()


@router.get("/{user_id}", response_model=schemas.UserRead)
def get_user(user_id: str, db: Session = Depends(database.get_db)):
    user = db.query(User).get(user_id)
    if not user: raise HTTPException(404, "User not found")
    return user


@router.put("/{user_id}", response_model=schemas.UserRead)
def update_user(user_id: str, u: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user = db.query(User).get(user_id)
    if not user: raise HTTPException(404, "Not found")
    user.username = u.username
    user.hashed_password = auth.get_password_hash(u.password)
    user.access = u.access
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(database.get_db)):
    user = db.query(User).get(user_id)
    if not user: raise HTTPException(404, "Not found")
    db.delete(user)
    db.commit()
    return {"detail": "Deleted"}
