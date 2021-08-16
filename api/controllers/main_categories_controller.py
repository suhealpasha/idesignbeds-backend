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

main_categories_controller = Blueprint('main_categories_controller', __name__)
CORS(main_categories_controller)
image_id = ''

@main_categories_controller.route("/v1/upload_category_image/category", methods=['POST'])
def image_upload():
    try:              
        my_file = request.files['images']
        now = datetime.now()
        filename = secure_filename(str(now)+'_'+my_file.filename)
        # path = request.host_url+('/static/uploads',filename)
        path = request.host_url+'static/uploads/'+filename
        if filename != '':
            
            file_ext = os.path.splitext(filename)[1]
            
            if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                return Response(json.dumps({
                        'Message': "Invalid file type!",                    
                    }), status=400)
            my_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return Response(json.dumps({
                        'Message': "File uploaded sucessfully!",
                        'path':path
                    }), status=200) 
            
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)

@main_categories_controller.route("/v1/register/main_category", methods=['POST'])
def register():
    try:        
        data = json.loads(request.data)
        
        for key in ['name','path','details','label']:
            if key not in data.keys():
                return Response(json.dumps({
                    'Error': "Missing parameter '" + key + "'"
                }), status=402)
                                
        category = api.models.MainCategories({
            'name':data['name'],
            'path':data['path'],
            'details':data['details'],
            'label':data['label']
                
        }) 
        db.session.add(category)
        db.session.commit()
        db.session.refresh(category)      
             
                
        category = api.models.MainCategories.query.filter_by(id=str(category.id)).first()
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
    
@main_categories_controller.route("/v1/list/main_categories", methods=['GET'])
def get_main_categories():
    try:
        
        cat = api.models.MainCategories.query.all()
        result=[]
        if cat:
            count = 0
            for data in cat:
                count = count + 1
                result.append({
                "name":data.name,                
                "p_id":data.id,
                "path":data.path,
                "details":data.details,
                "label":data.label,                
                "id":count,
                               
                })
        return Response(json.dumps({"result":result}),status=200)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)
    
@main_categories_controller.route("/v1/delete/main_category", methods=['POST'])
def delete_main_category():
    try:
        data = json.loads(request.data)
        print(data['id'])
        cat = api.models.MainCategories.query.filter_by(id=int(data['id'])).first()
        if cat:                       
            db.session.delete(cat)
            db.session.commit()
            cat_verify = api.models.MainCategories.query.filter_by(id=data['id']).first()
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

