from sqlalchemy.orm import validates
import secrets
from .base import Base, db

class ProductsImages(Base):    
    image = db.Column(db.String(200), nullable=False)
    product_image_id = db.Column(db.Integer,nullable = False)
    
    
    def __init__(self, product):
        super()
        self.image = product['image']
        self.product_image_id = product['product_image_id']
       