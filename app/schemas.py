from pydantic import BaseModel, EmailStr
from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    username: str
    password: str
    access: List[str] = []


class UserRead(BaseModel):
    id: UUID
    username: str
    access: List[str]
    created_at: datetime

    class Config:
        from_attributes = True


class TourCreate(BaseModel):
    name_ru: str
    name_en: str
    countries: List[str]
    duration: int
    dates: List[str]
    description_ru: str
    description_en: str
    price: int
    extra_costs_ru: List[dict] = []
    extra_costs_en: List[dict] = []
    accommodation: List[str]
    category: str
    tags: List[str]
    routes: List[Any]


class TourRead(TourCreate):
    id: UUID
    image_path: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    tour: UUID
    user: UUID
    citizenship: str
    phone: str
    tg: Optional[str]
    email: EmailStr
    date: str
    user_count: int
    comment: Optional[str] = ""


class OrderRead(OrderCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
