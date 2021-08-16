from sqlalchemy.orm import validates
import secrets
from .base import Base, db

class Baskets(Base):   
    color = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(200))
    total = db.Column(db.Numeric(precision=1))
    addons = db.Column(db.JSON)
    product_name = db.Column(db.String(100))
    basket_customer_id = db.Column(db.Integer,nullable = False)
    basket_product_id = db.Column(db.Integer,nullable = False)
    
    def __init__(self, product):
        super()
        self.color = product['color']
        self.size = product['size']
        self.total = product['total']   
        self.addons = product['addons'] 
        self.product_name = product['product_name']    
        self.basket_customer_id = product['basket_customer_id']
        self.basket_product_id = product['basket_product_id']
        
        