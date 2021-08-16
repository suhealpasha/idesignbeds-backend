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

addons_controller = Blueprint('addons_controller', __name__)
CORS(addons_controller)
image_id = ''


@addons_controller.route("/v1/register/addon", methods=['POST'])
def register():
    try:        
        data = json.loads(request.data)
        
        for key in ['addon_name']:
            if key not in data.keys():
                return Response(json.dumps({
                    'Error': "Missing parameter '" + key + "'"
                }), status=402)
                                
        addon = api.models.Addons({
            'addon_name':data['addon_name'],
            
                
        }) 
        db.session.add(addon)
        db.session.commit()
        db.session.refresh(addon)      
             
                
        addon = api.models.Addons.query.filter_by(id=str(addon.id)).first()
        if addon:
            return Response(json.dumps({
                    'Message': "addon registration successful"
                }), status=200)
        else:
            return Response(json.dumps({
                    'Error': "addon creation failed"
                }), status=400)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)    
    
@addons_controller.route("/v1/list/addons", methods=['GET'])
def get_addons():
    try:
        prod = api.models.Addons.query.all()
        result=[]
        if prod:
            count = 0
            for data in prod:
                count = count + 1
                result.append({
                "addon_name":data.addon_name,                          
                "p_id":data.id,
                "id":count,
                               
                })
        return Response(json.dumps({"result":result}),status=200)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)
    
@addons_controller.route("/v1/delete/addon", methods=['POST'])
def delete_addon():
    try:
        data = json.loads(request.data)
        print(data['id'])
        col = api.models.Addons.query.filter_by(id=int(data['id'])).first()
        if col:                       
            db.session.delete(col)
            db.session.commit()
            col_verify = api.models.Addons.query.filter_by(id=data['id']).first()
            if col_verify:
                return Response(json.dumps({"Error":'Addon deletion failed'}),status=400)
            else:
                return Response(json.dumps({"Message":'Addon deleted successfully'}),status=200)

        else: 
            return Response(json.dumps({"Error":'Addon not found'}),status=400)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)

