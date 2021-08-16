from sqlalchemy.orm import validates
import secrets
from .base import Base, db

class Categories(Base):    
    category_name = db.Column(db.String(100), unique=True, nullable=False)
    
    
    def __init__(self, product):
        super()
        self.category_name = product['category_name']
       