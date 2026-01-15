from sqlalchemy.orm import Session
from app import models, schemas

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def create_order(db: Session, order: schemas.OrderCreate, user_id: int):
    db_order = models.Order(user_id=user_id, status="pending", total_amount=0.0)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    total_amount = 0.0

    for item in order.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        
        if product:
            price = product.price
            total_amount += price * item.quantity
            
            db_order_item = models.OrderItem(
                order_id=db_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=price
            )
            db.add(db_order_item)

    db_order.total_amount = total_amount
    db.commit()
    db.refresh(db_order)
    
    return db_order