from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.orm import Session
from .. import schemas, models, database, auth

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def login(form_data: schemas.UserCreate, response: Response, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter_by(username=form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    access = auth.create_access_token(user.id)
    refresh = auth.create_refresh_token(user.id)
    response.set_cookie("access_token", access, httponly=True, secure=True, samesite="lax")
    response.set_cookie("refresh_token", refresh, httponly=True, secure=True, samesite="lax")
    return {"access_token": access, "refresh_token": refresh}


@router.post("/refresh", response_model=schemas.Token)
def refresh_tokens(response: Response, user: models.User = Depends(auth.get_user_from_refresh)):
    access = auth.create_access_token(user.id)
    refresh = auth.create_refresh_token(user.id)
    response.set_cookie("access_token", access, httponly=True, secure=True)
    response.set_cookie("refresh_token", refresh, httponly=True, secure=True)
    return {"access_token": access, "refresh_token": refresh}


@router.get("/auth-check", response_model=schemas.UserRead)
def auth_check(current_user: models.User = Depends(auth.get_current_user)):
    return current_user
