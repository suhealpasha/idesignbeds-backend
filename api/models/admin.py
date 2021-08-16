from sqlalchemy.orm import validates
import secrets
import validators
from .base import Base, db
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
class Admin(Base):
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)    
    key = db.Column(db.String(300), nullable=False)
 

    def __init__(self, user, expiration = 600):
        super()
        self.email = user['email']
        self.password = user['password']       
        self.key = user['key']
       
   