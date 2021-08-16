from sqlalchemy.orm import validates
from .base import Base, db
import os 
from werkzeug.security import generate_password_hash, check_password_hash
from api.helpers import crypto


class Users(Base):
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(50))
    status = db.Column(db.Boolean, nullable=False)
    user_type = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    external_res = db.Column(db.Integer, nullable = False)
    password_digest = db.Column(db.Text)
    users_user_id=db.Column(db.Integer,nullable=False)

    def __init__(self, user):
        super()
        self.description = user['description']
        self.name = user['name']
        self.user_type = user['user_type']
        self.external_res = user['external_res']
        self.status = user['status']
        self.username = user['username']
        
    def set_password(self, password):
        key = os.environ.get('XE_PASSWORD_KEY')
        encrypted = crypto.encrypt(key, str.encode(password))    
        self.password_digest = encrypted

    def check_password(self, password):
        key = os.environ.get('XE_PASSWORD_KEY')
        plain_text = crypto.decrypt(key, str.encode(self.password_digest))    
        return  password == plain_text.decode('utf-8')