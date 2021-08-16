from flask import Blueprint, request, Response
from flask_cors import CORS
import api.models
from api.helpers.raise_exception import raiseException
import json
import mysql.connector
from sshtunnel import SSHTunnelForwarder
from api import db
import time
from passlib.hash import sha256_crypt
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
import base64
# from Crypto.Cipher import AES
# from Crypto.Hash import SHA256
# from Crypto import Random
from smtplib import SMTPException
import smtplib
import os
from flask import jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

customer_controller = Blueprint('customer_controller', __name__)
CORS(customer_controller)

    
@customer_controller.route("/v1/customer/signup", methods=['POST'])
def register():
    try:       
        data = json.loads(request.data)
        for key in ['email','password','first_name','last_name','mobile','newsletter']:
            if key not in data.keys():
                return Response(json.dumps({
                    'Error': "Missing parameter '" + key + "'"
                }), status=402)
         
        key = Fernet.generate_key()
        encoded_message = str(data['password']).encode()
        f = Fernet(key)
        nl = ''
        if data['newsletter'] == True:
            nl = 1
        else:
            nl = 0
        encrypted_message = f.encrypt(encoded_message)  
            
        new_user = api.models.Customers({
            'email':data['email'],
            'password':encrypted_message,            
            'key':key,
            'first_name':data['first_name'],
            'last_name':data['last_name'],
            'newsletter':nl,
            'status':1,
            'mobile':data['mobile'],
            'home_address':None,
            'office_address':None     
            
        })
        user = api.models.Customers.query.filter_by(email=new_user.email).all()        
        if not user:
            db.session.add(new_user)
            db.session.commit()
            db.session.refresh(new_user)
            # access_token = create_access_token(identity=data['email'])
            # exisiting_user = api.models.Customers.query.filter_by(email=new_user.email).first()
            # token= api.models.Tokens({'api_key':str(access_token),'user_id':exisiting_user.id})
            # db.session.add(token)
            # db.session.commit()
            # db.session.refresh(token)  
           
            return Response(json.dumps({'Message': "User created successful",'status':200}), status=200)
            
                     
        else:
            return Response(json.dumps({
                    'Error': "User name already exist",'status':400
                }), status=200)
            
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)
    
@customer_controller.route("/v1/customer/signin", methods=['POST'])
def login():
    try:
        data = json.loads(request.data)
        for key in ['email','password']:
            if key not in data.keys():
                return Response(json.dumps({
                    'Error': "Missing parameter '" + key + "'"
                }), status=402)
            u_name = data['email']            
            pwsd = data['password']
           
          
        check = api.models.Customers.query.filter_by(email=u_name).first()
        if check is not None:
            user_id = check.id           
            key = check.key
            encoded_message = bytes(check.password, 'utf-8')            
            f = Fernet(key)
            decrypted_message = f.decrypt(encoded_message)
            test = (decrypted_message.decode())       
                                
            if(test == data['password'] ):                
                # token = api.models.Tokens.query.filter_by(user_id=str(check.id)).first()                
                return Response(json.dumps({'Message': "Login Success",'user_id':user_id,'email':u_name,'status':200}), status=200)
            else:
                return Response(json.dumps({'Error': "Invalid Password",'status':400}), status=200)
        else:
            return Response(json.dumps({'Error': "User not exist!",'status':400}), status=200)        
       
            
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)
    
@customer_controller.route("/v1/admin/forgotpassword", methods=['POST'])
def forgot_password():
    try:
        data = json.loads(request.data)
        for key in ['email']:
            if key not in data.keys():
                return Response(json.dumps({
                    'Error': "Missing parameter '" + key + "'"
                }), status=402)
            u_name = data['email']     
            
           
            
        check = api.models.Admin.query.filter_by(email=u_name).first()
        if check is not None:
            return Response(json.dumps({'Message': "Success",'id':check.id,'status':200}), status=200)
            
        else:
            return Response(json.dumps({'Error': "User not exist!",'status':400}), status=200)        
       
            
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)
    
@customer_controller.route("/v1/admin/resetpassword", methods=['POST'])
def reset_password():
    try:
        data = json.loads(request.data)
        for key in ['id']:
            if key not in data.keys():
                return Response(json.dumps({
                    'Error': "Missing parameter '" + key + "'"
                }), status=402)
            u_id = data['id']             
           
          
        check = api.models.Admin.query.filter_by(id=u_id).first()       
        if check is not None:
            key = Fernet.generate_key()
            encoded_message = str(data['password']).encode()
            f = Fernet(key)            
            encrypted_message = f.encrypt(encoded_message)        
            check.password=encrypted_message
            check.key=key
            db.session.commit()
            db.session.refresh(check)
            
            return Response(json.dumps({'Message': "Success",'status':200}), status=200)
            
        else:
            return Response(json.dumps({'Error': "User not exist!",'status':400}), status=200)        
       
            
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)
    
@customer_controller.route("/v1/customer/exist", methods=['POST'])
def customer_exist():
    try:
        data = json.loads(request.data)
        for key in ['email']:
            if key not in data.keys():
                return Response(json.dumps({
                    'Error': "Missing parameter '" + key + "'"
                }), status=402)
            u_id = data['email']             
           
         
        check = api.models.Customers.query.filter_by(email=u_id).first()       
        if check is None:            
            return Response(json.dumps({'Message': "Success",'status':200}), status=200)
            
        else:
            return Response(json.dumps({'Error': "User already exist!",'status':400}), status=200)        
       
            
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)
    
@customer_controller.route("/v1/customer/details", methods=['POST'])
def customer_details():
    try:
        data = json.loads(request.data)
        for key in ['email']:
            if key not in data.keys():
                return Response(json.dumps({
                    'Error': "Missing parameter '" + key + "'"
                }), status=402)
            u_id = data['email']             
           
        
        check = api.models.Customers.query.filter_by(email=u_id).first()       
        if check is not None: 
            data ={'first_name':check.first_name,
                                        'last_name':check.last_name,
                                        'mobile':check.mobile,
                                        'email':check.email,
                                        'office_address':check.office_address,
                                        'home_address':check.home_address,
                                        'userstatus':check.status}           
            return Response(json.dumps({'Message': "Success",
                                         'data':data,                                                                              
                                        'status':200}), status=200)
            
        else:
            return Response(json.dumps({'Error': "User already exist!",'status':400}), status=200)        
       
            
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)
    
@customer_controller.route("/v1/customer/edit_details", methods=['POST'])
def edit():
    try:
        data = json.loads(request.data)
        for key in ['email']:
            if key not in data.keys():
                return Response(json.dumps({
                    'Error': "Missing parameter '" + key + "'"
                }), status=402)
            u_id = data['email']             
           
         
        check = api.models.Customers.query.filter_by(email=u_id).first()       
        if check is not None: 
            check.office_address = data['office_address']
            check.home_address = data['home_address']
            db.session.commit()
            db.session.refresh(check)
            check = api.models.Customers.query.filter_by(email=u_id).first()  
            data ={'first_name':check.first_name,
                                        'last_name':check.last_name,
                                        'mobile':check.mobile,
                                        'email':check.email,
                                        'office_address':check.office_address,
                                        'home_address':check.home_address,
                                        'userstatus':check.status}  
            return Response(json.dumps({'Message': "Success",
                                         'data':data,                                                                              
                                        'status':200}), status=200)
            
        else:
            return Response(json.dumps({'Error': "User already exist!",'status':400}), status=200)        
       
            
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)
    
@customer_controller.route("/v1/list/customers", methods=['GET'])
def get_allcustomers():
    try:
        prod = api.models.Customers.query.all()
        result=[]
        if prod:
            count = 0
            for data in prod:
                count = count + 1
                result.append({
                "customer":data.first_name+' '+data.last_name,                
                "email":data.email,                
                "contact":data.mobile,
                "address":data.home_address, 
                "status":data.status,               
                "c_id":data.id,
                "id":count,
                               
                })
     
        return Response(json.dumps({"result":result}),status=200)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)

@customer_controller.route("/v1/delete/customer", methods=['POST'])
def delete_customer():
    try:
        data = json.loads(request.data)
        print(data['id'])
        col = api.models.Customers.query.filter_by(id=int(data['id'])).first()
        if col:                       
            db.session.delete(col)
            db.session.commit()
            col_verify = api.models.Customers.query.filter_by(id=data['id']).first()
            if col_verify:
                return Response(json.dumps({"Error":'Customer deletion failed'}),status=400)
            else:
                return Response(json.dumps({"Message":'Customer deleted successfully'}),status=200)

        else: 
            return Response(json.dumps({"Error":'Customer not found'}),status=400)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)