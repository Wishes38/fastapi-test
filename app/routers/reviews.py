from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.core.database import get_db
from fastapi.exceptions import HTTPException

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)

@router.post("/", response_model=schemas.Review)
def create_review(review: schemas.ReviewCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_review(db=db, review=review, user_id=user_id)

@router.get("/product/{product_id}", response_model=List[schemas.Review])
def read_reviews(product_id: int, db: Session = Depends(get_db)):
    return crud.get_reviews_by_product(db, product_id=product_id)

@router.get("/{review_id}", response_model=schemas.Review)
def read_review(review_id: int, db: Session = Depends(get_db)):
    db_review = crud.get_review(db, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Yorum bulunamadı")
    return db_review

@router.put("/{review_id}", response_model=schemas.Review)
def update_review(review_id: int, review_update: schemas.ReviewUpdate, db: Session = Depends(get_db)):
    db_review = crud.update_review(db, review_id, review_update)
    if not db_review:
        raise HTTPException(status_code=404, detail="Yorum bulunamadı")
    return db_review

@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = crud.delete_review(db, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Yorum bulunamadı")
    return {"message": "Yorum silindi."}