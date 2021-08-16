from sqlalchemy.orm import validates
import secrets
from .base import Base, db

class Reviews(Base):    
    name = db.Column(db.String(50), nullable=False)    
    image = db.Column(db.String(200), nullable=False)
    comment = db.Column(db.String(500))
    ratings = db.Column(db.Float(precision=2))
    review_product_id = db.Column(db.Integer,nullable = False)
    reviewer_customer_id = db.Column(db.Integer,nullable = False)
   
    
    def __init__(self, product):
        super()
        self.name = product['name']
        self.image = product['image']
        self.comment = product['comment']
        self.ratings = product['ratings']
        self.review_product_id = product['review_product_id']
        self.reviewer_customer_id = product['reviewer_customer_id']
     
        
        