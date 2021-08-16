from sqlalchemy.orm import validates
import secrets
from .base import Base, db

class MainCategories(Base):    
    name = db.Column(db.String(100), unique=True, nullable=False)
    path = db.Column(db.String(500), unique=True, nullable=False)
    details = db.Column(db.String(100), unique=True, nullable=False)
    label = db.Column(db.String(50), unique=True, nullable=False)
    
    def __init__(self, product):
        super()
        self.name = product['name']
        self.path = product['path']
        self.details = product['details']
        self.label = product['label']