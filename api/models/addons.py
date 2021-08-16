from sqlalchemy.orm import validates
import secrets
from .base import Base, db

class Addons(Base):    
    addon_name = db.Column(db.String(100), unique=True, nullable=False)
    
    
    def __init__(self, product):
        super()
        self.addon_name = product['addon_name']
       