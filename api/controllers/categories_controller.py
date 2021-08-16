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

categories_controller = Blueprint('categories_controller', __name__)
CORS(categories_controller)
image_id = ''


@categories_controller.route("/v1/register/category", methods=['POST'])
def register():
    try:        
        data = json.loads(request.data)
        
        for key in ['category_name']:
            if key not in data.keys():
                return Response(json.dumps({
                    'Error': "Missing parameter '" + key + "'"
                }), status=402)
                                
        category = api.models.Categories({
            'category_name':data['category_name']
                
        }) 
        db.session.add(category)
        db.session.commit()
        db.session.refresh(category)      
             
                
        category = api.models.Categories.query.filter_by(id=str(category.id)).first()
        if category:
            return Response(json.dumps({
                    'Message': "Category registration successful"
                }), status=200)
        else:
            return Response(json.dumps({
                    'Error': "Category creation failed"
                }), status=400)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)    
    
@categories_controller.route("/v1/list/categories", methods=['GET'])
def get_categories():
    try:
        
        cat = api.models.Categories.query.all()
        result=[]
        if cat:
            count = 0
            for data in cat:
                count = count + 1
                result.append({
                "category_name":data.category_name,                
                "p_id":data.id,
                "id":count,
                               
                })
        return Response(json.dumps({"result":result}),status=200)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)
    
@categories_controller.route("/v1/delete/category", methods=['POST'])
def delete_category():
    try:
        data = json.loads(request.data)
        print(data['id'])
        cat = api.models.Categories.query.filter_by(id=int(data['id'])).first()
        if cat:                       
            db.session.delete(cat)
            db.session.commit()
            cat_verify = api.models.Categories.query.filter_by(id=data['id']).first()
            if cat_verify:
                return Response(json.dumps({"Error":'Category deletion failed'}),status=400)
            else:
                return Response(json.dumps({"Message":'Category deleted successfully'}),status=200)

        else: 
            return Response(json.dumps({"Error":'Category not found'}),status=400)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)

