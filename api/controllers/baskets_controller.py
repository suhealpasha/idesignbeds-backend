from flask import Blueprint, request,redirect,url_for, Response,send_from_directory
from flask_cors import CORS
import api.models
from api.helpers.raise_exception import raiseException
from werkzeug.utils import secure_filename
import json
import mysql.connector
import os
from flask import current_app
from api import db
from datetime import datetime

baskets_controller = Blueprint('baskets_controller', __name__)
CORS(baskets_controller)
image_id = ''



@baskets_controller.route("/v1/register/basket", methods=['POST'])
def register():
    try:        
        data = json.loads(request.data)
        
        for key in ['color','size','addons',
                    'total','basket_customer_id','basket_product_id']:
            if key not in data.keys():
                return Response(json.dumps({
                    'Error': "Missing parameter '" + key + "'"
                }), status=402)
        
                
        product = api.models.Baskets({
                'color':data['color'],            
                'size':data['size'], 
                'addons':data['addons'],           
                'total':float(data['total']),
                "product_name":data['product_name'],
                'basket_customer_id':int(data['basket_customer_id']),
                'basket_product_id':int(data['basket_product_id'])           
            }) 
        db.session.add(product)
        db.session.commit()
        db.session.refresh(product)      
                
                    
        product = api.models.Baskets.query.filter_by(id=int(product.id)).first()
        if product:
            return Response(json.dumps({
                        'Message': "Basket added successful"
                    }), status=200)
        else:
            return Response(json.dumps({
                        'Error': "Adding Basket failed"
                    }), status=400)
        
        
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)    
    
@baskets_controller.route("/v1/list/customer_basket", methods=['POST'])
def get_baskets_by_customer():
    try:
        data = json.loads(request.data)        
        for key in ['id']:
            if key not in data.keys():
                return Response(json.dumps({
                    'Error': "Missing parameter '" + key + "'"
                }), status=402)
        prod = api.models.Baskets.query.filter_by(basket_customer_id=int(data['id'])).all()
        
        mydata=[]
        if prod:
            count = 0
            for data in prod:
                count = count + 1
                mydata.append({                                
                "basket_product_id":data.basket_product_id,  
                "product_name":data.product_name,
                "size":data.size,
                "addons":data.addons,
                "total":str(data.total),
                "color":data.color,             
                "p_id":data.id,               
                "id":count,                              
                })
            if mydata:            
                return Response(json.dumps({
                    'Message': "User Basket",
                    "data":mydata
                }), status=200)
            else: 
                return Response(json.dumps({"Error":'Basket no items'}),status=200)
        else:    
            return Response(json.dumps({"Error":'No Basket'}),status=400)
    
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)
    
@baskets_controller.route("/v1/remove/basket_item", methods=['POST'])
def delete_basket():
    try:
        data = json.loads(request.data)
        print(data['id'])
        col = api.models.Baskets.query.filter_by(id=int(data['id'])).first()
        if col:                       
            db.session.delete(col)
            db.session.commit()
            rev_verify = api.models.Baskets.query.filter_by(id=data['id']).first()
            if rev_verify:
                return Response(json.dumps({"Error":'Basket deletion failed'}),status=400)
            else:                
                return Response(json.dumps({"Message":'Basket deleted successfully'}),status=200)

        else: 
            return Response(json.dumps({"Error":'Basket not found'}),status=400)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)
    
@baskets_controller.route("/v1/delete/basket", methods=['POST'])
def delete_all_basket():
    try:
        data = json.loads(request.data)
        
        col = api.models.Baskets.query.filter_by(basket_customer_id=int(data['id'])).all()
        if col:
            for c in col:                       
                db.session.delete(c)
                db.session.commit()                              
            return Response(json.dumps({"Message":'Basket deleted successfully'}),status=200)

        else: 
            return Response(json.dumps({"Error":'Basket not found'}),status=400)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)
    
