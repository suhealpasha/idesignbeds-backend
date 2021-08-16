from sqlalchemy.orm import validates
import secrets
from .base import Base, db

class Colors(Base):    
    color_name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(15), nullable=False)
    
    
    def __init__(self, product):
        super()
        self.color_name = product['color_name']
        self.code = product['code']
       