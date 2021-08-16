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

reviews_controller = Blueprint('reviews_controller', __name__)
CORS(reviews_controller)
image_id = ''

def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@reviews_controller.route('/static/uploads/<filename>', methods=['GET', 'POST'])
def display_image(filename):
    root = str(current_app.root_path)
    root = root[:-4]
    uploads = os.path.join(root,current_app.config['UPLOAD_FOLDER'])    
    return send_from_directory(directory=uploads, path=filename)
    # return redirect(url_for('static', filename='uploads/' + filename), code=301)


@reviews_controller.route("/v1/upload_profile_image/review", methods=['POST'])
def profile_upload():
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

@reviews_controller.route("/v1/register/review", methods=['POST'])
def register():
    try:        
        data = json.loads(request.data)
        
        for key in ['name','id','customer_id',
                    'comment','path','ratings']:
            if key not in data.keys():
                return Response(json.dumps({
                    'Error': "Missing parameter '" + key + "'"
                }), status=402)
        
          
        customer = api.models.Customers.query.filter_by(id=int(data['customer_id'])).first() 
        
        if customer:    
                
            review = api.models.Reviews({
                'name':data['name'],            
                'comment':data['comment'],  
                'ratings':data['ratings'],          
                'image':data['path'][0],                
                'review_product_id':int(data['id']),
                'reviewer_customer_id':int(data['customer_id'])         
            }) 
            db.session.add(review)
            db.session.commit()
            db.session.refresh(review)      
                
                    
            new_review = api.models.Reviews.query.filter_by(id=str(review.id)).first()
            if new_review:
                product = api.models.Reviews.query.all()
                ratings = 0
                count = 0
                print(count)
                for p in product:
                    print(data['id'],review.review_product_id)
                    if data['id'] == review.review_product_id:
                        count = count + 1
                        ratings = ratings + p.ratings 
                        print(count,ratings,p.ratings)
                avg_ratings = ratings / count
                print(avg_ratings)
                product = api.models.Products.query.filter_by(id=int(review.review_product_id)).first()  
                product.ratings = avg_ratings
                db.session.commit()
                db.session.refresh(product)       
                return Response(json.dumps({
                        'Message': "Review registration successful"
                    }), status=200)
            else:
                return Response(json.dumps({
                        'Error': "Review creation failed"
                    }), status=400)
        else:
            return Response(json.dumps({
                        'Error': "Invalid customer Id"
                    }), status=400)
        
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)    
    
@reviews_controller.route("/v1/list/reviews", methods=['GET'])
def get_reviews():
    try:
        prod = api.models.Reviews.query.all()
        result=[]
        if prod:
            count = 0
            for data in prod:
                count = count + 1
                result.append({
                "name":data.name,                
                "comment":data.comment,               
                "p_id":data.id,
                "ratings":str(data.ratings),
                "id":count,
                "review_product_id":data.review_product_id               
                })
     
        return Response(json.dumps({"result":result}),status=200)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)
    
@reviews_controller.route("/v1/delete/review", methods=['POST'])
def delete_review():
    try:
        data = json.loads(request.data)
        print(data['id'])
        col = api.models.Reviews.query.filter_by(id=int(data['id'])).first()
        if col:                       
            db.session.delete(col)
            db.session.commit()
            rev_verify = api.models.Reviews.query.filter_by(id=data['id']).first()
            if rev_verify:
                return Response(json.dumps({"Error":'Review deletion failed'}),status=400)
            else:
                return Response(json.dumps({"Message":'Review deleted successfully'}),status=200)

        else: 
            return Response(json.dumps({"Error":'Review not found'}),status=400)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)
    
@reviews_controller.route("/v1/list/review_by_product", methods=['POST'])
def review_by_product():
    try:
        data = json.loads(request.data)
        
        col = api.models.Reviews.query.filter_by(review_product_id=int(data['id'])).all()
        
        if col:                       
            count = 0
            result = []
            for data in col:
                count = count + 1
                result.append({
                "name":data.name,                
                "comment":data.comment,               
                "p_id":data.id,
                "ratings":str(data.ratings),
                "id":count,    
                "image":data.image,
                "product_id":data.review_product_id,
                'date':str(data.created_at)                           
                })
            if col:                
                return Response(json.dumps({"result":result}),status=200)
            else:
                return Response(json.dumps({"Message":'No Reviews'}),status=400)

        else: 
            return Response(json.dumps({"Error":'Review not found'}),status=400)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)
    
@reviews_controller.route("/v1/list/review_by_customer", methods=['POST'])
def review_by_customer():
    try:
        data = json.loads(request.data)
        
        col = api.models.Reviews.query.filter_by(reviewer_customer_id=int(data['id'])).all()
        
        if col:                       
            count = 0
            result = []
            for data in col:
                count = count + 1
                result.append({
                "name":data.name,                
                "comment":data.comment,               
                "p_id":data.id,
                "ratings":str(data.ratings),
                "id":count,    
                "image":data.image,
                "product_id":data.review_product_id,
                'date':str(data.created_at)                           
                })
            if col:                
                return Response(json.dumps({"result":result}),status=200)
            else:
                return Response(json.dumps({"Message":'No Reviews'}),status=400)

        else: 
            return Response(json.dumps({"Error":'Review not found'}),status=400)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)

