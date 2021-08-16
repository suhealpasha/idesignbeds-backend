from sqlalchemy.orm import validates
import secrets
import validators
from .base import Base, db

class Tokens(Base):
    api_key = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer,nullable=False)
    
    def __init__(self, device):
        super()
        self.api_key = device['api_key']
        self.user_id = device['user_id']
   