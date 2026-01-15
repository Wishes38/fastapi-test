from sqlalchemy.orm import Session
from app import models, schemas

def create_review(db: Session, review: schemas.ReviewCreate, user_id: int):
    db_review = models.Review(**review.model_dump(), user_id=user_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_reviews_by_product(db: Session, product_id: int):
    return db.query(models.Review).filter(models.Review.product_id == product_id).all()