from datetime import datetime, timedelta

from fastapi import HTTPException, Depends, Cookie
from passlib.context import CryptContext
from jose import jwt, JWTError
from sqlalchemy.orm import Session
import database.database as database
from models.models import User
from settings.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(user_id):
    return create_token(
        {"sub": str(user_id)},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def create_refresh_token(user_id):
    return create_token(
        {"sub": str(user_id)},
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )


def get_current_user(
        access_token: str = Cookie(None, alias="access_token"),
        db: Session = Depends(database.get_db)
):
    if not access_token:
        print(access_token)
        raise HTTPException(status_code=401, detail="Missing access token")
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        user = db.query(User).get(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")


def get_user_from_refresh(
        refresh_token: str = Cookie(None, alias="refresh_token"),
        db: Session = Depends(database.get_db)
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        user = db.query(User).get(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
