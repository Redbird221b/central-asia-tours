import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    access = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)


class Tour(Base):
    __tablename__ = "tours"
    __table_args__ = {"extend_existing": True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name_ru = Column(String, nullable=False)
    name_en = Column(String, nullable=False)
    countries = Column(JSON, default=list)
    duration = Column(Integer)
    dates = Column(JSON, default=list)
    image_path = Column(String)
    description_ru = Column(String)
    description_en = Column(String)
    price = Column(Integer)
    extra_costs_ru = Column(JSON, default=list)
    extra_costs_en = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    accommodation = Column(JSON, default=list)
    category = Column(String)
    tags = Column(JSON, default=list)
    routes = Column(JSON, default=list)


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, autoincrement=True)
    tour_id = Column(UUID(as_uuid=True), ForeignKey("tours.id"), nullable=False)
    citizenship = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    tg = Column(String, default="")
    email = Column(String, nullable=False)
    date = Column(String, nullable=False)
    user_count = Column(Integer, default=1)
    comment = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    tour = relationship("Tour")
