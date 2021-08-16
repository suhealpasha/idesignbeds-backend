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

products_controller = Blueprint('products_controller', __name__)
CORS(products_controller)
image_id = ''

def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@products_controller.route('/static/uploads/<filename>', methods=['GET', 'POST'])
def display_image(filename):
    print(filename)
    root = str(current_app.root_path)
    root = root[:-4]
    uploads = os.path.join(root,current_app.config['UPLOAD_FOLDER'])  
    print(uploads)  
    return send_from_directory(directory=uploads, filename=filename)
    # return redirect(url_for('static', filename='uploads/' + filename), code=301)


@products_controller.route("/v1/upload_image/product", methods=['POST'])
def upload():
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
            print(type(request.values['edit']))
            if int(request.values['edit']) == 0:    
                
                my_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                return Response(json.dumps({
                        'Message': "File uploaded sucessfully!",
                        'path':path
                    }), status=200) 
            else:
                temp = request.values['old_name']
                temp = temp.split('/')[-1]
                # os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], temp))    
                my_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], temp))
                return Response(json.dumps({
                        'Message': "File uploaded sucessfully!",
                        'path':path
                    }), status=200) 
                     
        # newFile = api.models.ProductsImages({
        #     'image':path,
        #     'product_image_id':None
        # })
        # db.session.add(newFile)
        # db.session.commit()
        # db.session.refresh(newFile) 
        # image = newFile.id 
        # image_id = image.id
        
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)

@products_controller.route("/v1/register/product", methods=['POST'])
def register():
    try:        
        data = json.loads(request.data)
        
        for key in ['productName','addons','unit','category','size',
                    'color','productDetails','specification','productDescription','quantity','categoryId','path']:
            if key not in data.keys():
                return Response(json.dumps({
                    'Error': "Missing parameter '" + key + "'"
                }), status=402)
        
                        
        product = api.models.Products({
            'product_name':data['productName'],            
            'addons':data['addons'],
            'unit':data['unit'],
            'category_id':data['categoryId'],
            'product_description':data['productDetails'],
            'category':data['category'],
            'quantity':int(data['quantity']), 
            'sold_out':0,          
            'basket':0,
            'ratings':0.0,
            'product_details':data['productDescription'],
            'specification':data['specification'],
            'product_images':data['path'],
            'colors':data['color'],
            'sizes':data['size']            
        }) 
        db.session.add(product)
        db.session.commit()
        db.session.refresh(product)      
             
                
        product = api.models.Products.query.filter_by(id=str(product.id)).first()
        if product:
            return Response(json.dumps({
                    'Message': "Product registration successful"
                }), status=200)
        else:
            return Response(json.dumps({
                    'Error': "Product creation failed"
                }), status=400)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)    
    
@products_controller.route("/v1/list/products", methods=['GET'])
def get_products():
    try:
        prod = api.models.Products.query.all()
        result=[]
        if prod:
            count = 0
            for data in prod:
                count = count + 1
                result.append({
                "product_name":data.product_name,                
                "addons":data.addons,                
                "created_date":str(data.created_at).split(" ")[0],
                "unit":data.unit, 
                "product_description":data.product_description, 
                "category":data.category, 
                "sold_out":data.sold_out,
                "quantity":data.quantity,                
                "basket":data.basket, 
                "ratings":data.ratings,
                "product_details":data.product_details, 
                "specification":data.specification, 
                "product_images":data.product_images,
                'colors':data.colors,
                'sizes':data.sizes,
                "p_id":data.id,
                "category_id":data.category_id,
                "id":count,
                               
                })
     
        return Response(json.dumps({"result":result}),status=200)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)

@products_controller.route("/v1/update/product", methods=['POST'])
def update_product():
    try:
        data = json.loads(request.data)
        print(data)
        for key in ['id']:
            if key not in data.keys():
                return Response(json.dumps({
                    'Error': "Missing parameter '" + key + "'"
                }), status=402)
        product = api.models.Products.query.filter_by(id=int(data['id'])).first()
        print(product)
        if product:
            if 'productName' in data.keys():
                product.product_name = data['productName']
            if 'size' in data.keys():
                product.sizes=data['size']
            if 'color' in data.keys():
                product.colors=data['color']
            if 'addons' in data.keys():
                product.addons=data['addons']
            if 'productDetails' in data.keys():
                product.product_details=data['productDetails']
            if 'specification' in data.keys():
                product.specification=data['specification']            
            if 'productDescription' in data.keys():
                product.product_description=data['productDescription']
            if 'quantity' in data.keys():
                product.quantity=data['quantity']
            if 'unit' in data.keys():
                product.unit=data['unit']
           
                 
            db.session.commit()
            db.session.refresh(product)
            product = api.models.Products.query.filter_by(id=data['id']).first()
            if product:
                return Response(json.dumps({
                    'Message': "Successfully updated"
                }), status=200)
        else: 
            return Response(json.dumps({"Error":'Product not found'}),status=400)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)

# @products_controller.route("/v1/list/cat_products", methods=['POST'])
# def get_cat_products():
#     try:
#         for key in ['id']:
#             if key not in data.keys():
#                 return Response(json.dumps({
#                     'Error': "Missing parameter '" + key + "'"
#                 }), status=402)
#         prod = api.models.Products.query.filter_by(category_id=int(data['id'])).all()
#         result=[]
#         if prod:
#             count = 0
#             for data in prod:
#                 count = count + 1
#                 result.append({
#                 "product_name":data.product_name,                
#                 "addons":data.addons,                
#                 "created_date":str(data.created_at).split(" ")[0],
#                 "unit":data.unit, 
#                 "product_description":data.product_description, 
#                 "category":data.category, 
#                 "quantity":data.quantity,                
#                 "basket":data.basket, 
#                 "product_details":data.product_details, 
#                 "specification":data.specification, 
#                 "product_images":data.product_images,
#                 'colors':data.colors,
#                 'sizes':data.sizes,
#                 "p_id":data.id,
#                 "id":count,
                               
#                 })
     
#         return Response(json.dumps({"result":result}),status=200)
#     except Exception as e:
#         if e.__class__.__name__ == "IntegrityError":
#             db.session.rollback()
#         return raiseException(e)

@products_controller.route("/v1/product/details", methods=['POST'])
def product_details():
    try:
        data = json.loads(request.data)
        print(data)
        for key in ['id']:
            if key not in data.keys():
                return Response(json.dumps({
                    'Error': "Missing parameter '" + key + "'"
                }), status=402)
        product = api.models.Products.query.filter_by(id=int(data['id'])).first()
        result=[]
        if product:
            result.append({
                "product_name":product.product_name,                
                "addons":product.addons,                
                "created_date":str(product.created_at).split(" ")[0],
                "unit":product.unit, 
                "product_description":product.product_description, 
                "category":product.category, 
                "quantity":product.quantity,                
                "basket":product.basket, 
                "ratings":product.ratings,
                "product_details":product.product_details, 
                "specification":product.specification, 
                "product_images":product.product_images,
                'colors':product.colors,
                'sizes':product.sizes,
                "p_id":product.id})  
            if product:
                return Response(json.dumps({
                    'Message': "Product Details",
                    "data":result
                }), status=200)
        else: 
            return Response(json.dumps({"Error":'Product not found'}),status=400)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)