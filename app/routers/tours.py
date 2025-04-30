import os
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from .. import schemas, models, database
from ..settings import settings

IMAGES_DIR = "images"
router = APIRouter(prefix="/tours")


@router.post("/", response_model=schemas.TourRead)
def create_tour(
        tour: schemas.TourCreate,
        image: UploadFile = File(...),
        db: Session = Depends(database.get_db)
):
    db_tour = models.Tour(**tour.dict(), image_path=None)
    db.add(db_tour)
    db.commit()
    db.refresh(db_tour)

    tour_folder = os.path.join(IMAGES_DIR, str(db_tour.id))
    os.makedirs(tour_folder, exist_ok=True)
    filename = f"{uuid4().hex}_{image.filename}"
    path = os.path.join(tour_folder, filename)
    with open(path, "wb") as f: f.write(image.file.read())

    db_tour.image_path = f"/images/{db_tour.id}/{filename}"
    db.commit()
    db.refresh(db_tour)
    return db_tour


@router.get("/", response_model=List[schemas.TourRead])
def list_tours(
        count: Optional[int] = Query(None),
        db: Session = Depends(database.get_db)
):
    q = db.query(models.Tour).order_by(models.Tour.created_at.desc())
    return q.limit(count).all() if count else q.all()


@router.get("/{tour_id}", response_model=schemas.TourRead)
def get_tour(tour_id: str, db: Session = Depends(database.get_db)):
    t = db.query(models.Tour).get(tour_id)
    if not t: raise HTTPException(404, "Not found")
    return t


@router.get("/category/{category}", response_model=List[schemas.TourRead])
def list_by_category(
        category: str,
        count: Optional[int] = Query(None),
        db: Session = Depends(database.get_db)
):
    q = db.query(models.Tour).filter_by(category=category).order_by(models.Tour.created_at.desc())
    return q.limit(count).all() if count else q.all()


@router.put("/{tour_id}", response_model=schemas.TourRead)
def update_tour(tour_id: str, tour: schemas.TourCreate, db: Session = Depends(database.get_db)):
    t = db.query(models.Tour).get(tour_id)
    if not t: raise HTTPException(404, "Not found")
    for k, v in tour.dict().items(): setattr(t, k, v)
    db.commit()
    db.refresh(t)
    return t


@router.delete("/{tour_id}")
def delete_tour(tour_id: str, db: Session = Depends(database.get_db)):
    t = db.query(models.Tour).get(tour_id)
    if not t: raise HTTPException(404, "Not found")
    db.delete(t)
    db.commit()
    return {"detail": "Deleted"}
