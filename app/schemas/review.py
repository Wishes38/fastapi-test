from pydantic import BaseModel

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