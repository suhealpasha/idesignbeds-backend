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

colors_controller = Blueprint('colors_controller', __name__)
CORS(colors_controller)
image_id = ''


@colors_controller.route("/v1/register/color", methods=['POST'])
def register():
    try:        
        data = json.loads(request.data)
        
        for key in ['color_name','code']:
            if key not in data.keys():
                return Response(json.dumps({
                    'Error': "Missing parameter '" + key + "'"
                }), status=402)
                                
        color = api.models.Colors({
            'color_name':data['color_name'],
            'code':data['code']
                
        }) 
        db.session.add(color)
        db.session.commit()
        db.session.refresh(color)      
             
                
        color = api.models.Colors.query.filter_by(id=str(color.id)).first()
        if color:
            return Response(json.dumps({
                    'Message': "color registration successful"
                }), status=200)
        else:
            return Response(json.dumps({
                    'Error': "color creation failed"
                }), status=400)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)    
    
@colors_controller.route("/v1/list/colors", methods=['GET'])
def get_colors():
    try:
        prod = api.models.Colors.query.all()
        result=[]
        if prod:
            count = 0
            for data in prod:
                count = count + 1
                result.append({
                "color_name":data.color_name,    
                "code":data.code,            
                "p_id":data.id,
                "id":count,
                               
                })
        return Response(json.dumps({"result":result}),status=200)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)
    
@colors_controller.route("/v1/delete/color", methods=['POST'])
def delete_color():
    try:
        data = json.loads(request.data)
        print(data['id'])
        col = api.models.Colors.query.filter_by(id=int(data['id'])).first()
        if col:                       
            db.session.delete(col)
            db.session.commit()
            col_verify = api.models.Colors.query.filter_by(id=data['id']).first()
            if col_verify:
                return Response(json.dumps({"Error":'Color deletion failed'}),status=400)
            else:
                return Response(json.dumps({"Message":'Color deleted successfully'}),status=200)

        else: 
            return Response(json.dumps({"Error":'Color not found'}),status=400)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)

