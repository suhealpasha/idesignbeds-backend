from sqlalchemy.orm import validates
import secrets
from .base import Base, db

class Orders(Base): 
    products = db.Column(db.JSON,nullable = False)  
    customer_details = db.Column(db.JSON,nullable = False) 
    order_no = db.Column(db.Integer,nullable = False)
    total = db.Column(db.Numeric(precision=1))
    items = db.Column(db.Integer,nullable = False)
    status = db.Column(db.String(20),nullable = False)
    payment = db.Column(db.String(20),nullable = False)
    order_customer_id = db.Column(db.Integer,nullable = False)
    stripe_customer_id = db.Column(db.String(100),nullable = False)
    
    def __init__(self, product):
        super()
        self.products = product['products']
        self.customer_details = product['customer_details']
        self.order_no = product['order_no']
        self.status = product['status']
        self.items = product['items']
        self.payment = product['payment']
        self.total = product['total']        
        self.order_customer_id = product['order_customer_id']
        self.stripe_customer_id = product['stripe_customer_id']
        
        
        