from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.orm import Session
from models.models import User
from schemas.schemas import UserCreate, UserRead, Token
import database.database as database
import auth.auth as auth

router = APIRouter()


@router.post("/login", response_model=Token)
def login(form_data: UserCreate, response: Response, db: Session = Depends(database.get_db)):
    user = db.query(User).filter_by(username=form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    access = auth.create_access_token(user.id)
    refresh = auth.create_refresh_token(user.id)
    response.set_cookie("access_token", access, httponly=True, secure=True, samesite="none")
    response.set_cookie("refresh_token", refresh, httponly=True, secure=True, samesite="none")
    return {"access_token": access, "refresh_token": refresh, "access": user.access}


@router.post("/refresh", response_model=Token)
def refresh_tokens(response: Response, user: User = Depends(auth.get_user_from_refresh)):
    access = auth.create_access_token(user.id)
    refresh = auth.create_refresh_token(user.id)
    response.set_cookie("access_token", access, httponly=True, secure=True, samesite="none")
    response.set_cookie("refresh_token", refresh, httponly=True, secure=True, samesite="none")
    return {"access_token": access, "refresh_token": refresh}


@router.get("/auth-check", response_model=UserRead)
def auth_check(current_user: User = Depends(auth.get_current_user)):
    return current_user
