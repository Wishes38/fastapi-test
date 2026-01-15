from pydantic import BaseModel
from typing import Optional

class ReviewBase(BaseModel):
    rating: int
    comment: str
    product_id: int

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True

class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None