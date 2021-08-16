from sqlalchemy.orm import validates
import secrets
from .base import Base, db

class Products(Base):    
    product_name = db.Column(db.String(50), unique=True, nullable=False)    
    category_id = db.Column(db.Integer, nullable=False)  
    unit = db.Column(db.String(50), nullable=False)
    product_description = db.Column(db.String(50))
    category = db.Column(db.String(50))
    quantity = db.Column(db.Integer, nullable=False)   
    sold_out = db.Column(db.Integer, nullable=False)    
    basket = db.Column(db.Integer,nullable = False)   
    ratings = db.Column(db.Float(precision=2)) 
    product_details = db.Column(db.String(1000))
    specification = db.Column(db.String(1000))
    product_images = db.Column(db.JSON)
    colors = db.Column(db.JSON)
    sizes = db.Column(db.JSON)
    addons = db.Column(db.JSON)
    
    def __init__(self, product):
        super()
        self.product_name = product['product_name']
        self.category_id = product['category_id']
        self.addons = product['addons']
        self.unit = product['unit']
        self.product_description = product['product_description']
        self.category = product['category']
        self.quantity = product['quantity'] 
        self.sold_out = product['sold_out']       
        self.basket = product['basket']   
        self.ratings = product['ratings']       
        self.product_details = product['product_details']
        self.specification = product['specification']
        self.product_images = product['product_images']
        self.colors = product['colors']
        self.sizes = product['sizes']
        