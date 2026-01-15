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

def get_review(db: Session, review_id: int):
    return db.query(models.Review).filter(models.Review.id == review_id).first()

def delete_review(db: Session, review_id: int):
    db_review = get_review(db, review_id)
    if db_review:
        db.delete(db_review)
        db.commit()
    return db_review

def update_review(db: Session, review_id: int, review_update: schemas.ReviewUpdate):
    db_review = get_review(db, review_id)
    if not db_review:
        return None
    
    update_data = review_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_review, key, value)
        
    db.commit()
    db.refresh(db_review)
    return db_review