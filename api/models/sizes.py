from sqlalchemy.orm import validates
import secrets
from .base import Base, db

class Sizes(Base):    
    size = db.Column(db.String(200), nullable=False)
    dimension = db.Column(db.String(200), nullable=False)
    product_size_id = db.Column(db.Integer,nullable = False)
    
    
    def __init__(self, product):
        super()
        self.size = product['size']
        self.dimension = product['dimension']
        self.product_size_id = product['product_size_id']
       