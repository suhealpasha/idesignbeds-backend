from sqlalchemy.orm import validates
import secrets
import validators
from .base import Base, db
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
class Customers(Base):
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)    
    key = db.Column(db.String(300), nullable=False)
    newsletter = db.Column(db.Integer)
    first_name = db.Column(db.String(50),  nullable=False)
    last_name = db.Column(db.String(50),nullable=False)
    status = db.Column(db.Integer)
    mobile = db.Column(db.String(50), nullable=False)
    home_address = db.Column(db.String(200))
    office_address = db.Column(db.String(200))

    def __init__(self, user, expiration = 600):
        super()
        self.email = user['email']
        self.password = user['password']       
        self.key = user['key']
        self.newsletter = user['newsletter']
        self.first_name = user['first_name']
        self.last_name = user['last_name']
        self.mobile = user['mobile']
        self.office_address = user['office_address']
        self.home_address = user['home_address']
        self.status = user['status']
       
   