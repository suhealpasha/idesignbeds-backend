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
import stripe

stripe.api_key = 'sk_test_51JNaGjSFPjCDuSEELRe2JWnPfD6aDJGl6MQvRRIvl1PKHSeDZp1KhTIvV3nmuvesvysZzF4LawBENW8gTvhP0pU200miUBsK8m'

# endpoint_secret = 'sk_test_51JNaGjSFPjCDuSEELRe2JWnPfD6aDJGl6MQvRRIvl1PKHSeDZp1KhTIvV3nmuvesvysZzF4LawBENW8gTvhP0pU200miUBsK8m'

orders_controller = Blueprint('orders_controller', __name__)
CORS(orders_controller)


@orders_controller.route("/v1/order/place", methods=['POST'])
def register():
    try:        
        data = json.loads(request.data)
        
        for key in ['id','products','items','total','stripe_customer_id','customer_details']:
            if key not in data.keys():
                return Response(json.dumps({
                    'Error': "Missing parameter '" + key + "'"
                }), status=402)
        
        descending = api.models.Orders.query.all() 
              
        last_item = 1
        if descending:   
            if len(descending) > 1:                
                descending = descending[-1]                                                   
                last_item = int(descending.id) + 1                                  
                     
            else:   
                descending = descending[0]                                
                last_item = int(descending.id) + 1                
                                            
                
           
        now = datetime.today().strftime('%Y%m%d')        
        order_no = str(now)+str(last_item)
        
        order = api.models.Orders({
                'order_no':order_no,            
                'items':data['items'],            
                'total':float(data['total']),
                'payment':'stripe',
                'stripe_customer_id':data['stripe_customer_id'],
                'order_customer_id':data['id'],
                'products':data['products'],
                'customer_details':data['customer_details'],
                'status':'placed'           
            }) 
        db.session.add(order)
        db.session.commit()
        db.session.refresh(order)                   
        order = api.models.Orders.query.filter_by(id=int(order.id)).first()
        if order:
            product_list = order.products
            for p in product_list:
                prod_id = p['basket_product_id']                
                product = api.models.Products.query.filter_by(id=int(prod_id)).first()
                exsisting_quantity = product.quantity
                exsisting_sold_out = product.sold_out
                product.quantity = int(exsisting_quantity) - 1
                product.sold_out = int(exsisting_sold_out) + 1
                db.session.add(product)
                db.session.commit()
                db.session.refresh(product)               
            return Response(json.dumps({
                        'Message': "Order added successful",
                        'order_no':order.order_no
                    }), status=200)
        else:
            return Response(json.dumps({
                        'Error': "Adding Order failed"
                    }), status=400)
        
        
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)    
    
@orders_controller.route("/v1/list/customer_orders", methods=['POST'])
def get_orders_by_customer():
    try:
        data = json.loads(request.data)        
        for key in ['id']:
            if key not in data.keys():
                return Response(json.dumps({
                    'Error': "Missing parameter '" + key + "'"
                }), status=402)
        prod = api.models.Orders.query.filter_by(order_customer_id=int(data['id'])).all()
        
        mydata=[]
        if prod:
            count = 0
            for data in prod:
                count = count + 1
                mydata.append({  
                "order_no":data.order_no,                                            
                "products":data.products, 
                "payment":data.payment, 
                "items":data.items,
                "total":str(data.total),
                "status":data.status, 
                "created_at":str(data.created_at),
                "updated_at":str(data.updated_at),            
                "p_id":data.id,               
                "id":count                             
                })
            if mydata:            
                return Response(json.dumps({
                    'Message': "User Orders",
                    "data":mydata
                }), status=200)
            else: 
                return Response(json.dumps({"Error":'No orders'}),status=200)
        else:    
            return Response(json.dumps({"Error":'No Orders'}),status=400)
    
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)
    
@orders_controller.route("/v1/list/orders", methods=['GET'])
def list_orders():
    try:
        
        prod = api.models.Orders.query.all()  
             
        mydata=[]
        if prod:
            count = 0
            for data in prod:                            
                
                count = count + 1                
                mydata.append({  
                "name": data.customer_details['first_name'] +' '+data.customer_details['last_name'],
                "order_no":data.order_no,                                            
                "products":data.products,  
                "customer_details":data.customer_details,
                "stripe_customer_id":data.stripe_customer_id,
                "payment":data.payment,
                "items":data.items,
                "total":str(data.total),
                "status":data.status, 
                "created_at":str(data.created_at),
                "updated_at":str(data.updated_at),            
                "p_id":data.id,               
                "id":count                             
                })
            if mydata:            
                return Response(json.dumps({
                    'Message': "User Orders",
                    "data":mydata
                }), status=200)
        else:             
            return Response(json.dumps({"Error":'No orders',"data":mydata}),status=200)
        
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)
    
@orders_controller.route("/v1/delete/order", methods=['POST'])
def delete_order():
    try:
        data = json.loads(request.data)
        print(data['id'])
        col = api.models.Orders.query.filter_by(id=int(data['id'])).first()
        if col:                       
            db.session.delete(col)
            db.session.commit()
            col_verify = api.models.Orders.query.filter_by(id=data['id']).first()
            if col_verify:
                return Response(json.dumps({"Error":'Order deletion failed'}),status=400)
            else:
                return Response(json.dumps({"Message":'Order deleted successfully'}),status=200)

        else: 
            return Response(json.dumps({"Error":'Order not found'}),status=400)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)
    
@orders_controller.route("/v1/update/order", methods=['POST'])
def update_order():
    try:
        data = json.loads(request.data)
        print(data)
        for key in ['id','status']:
            if key not in data.keys():
                return Response(json.dumps({
                    'Error': "Missing parameter '" + key + "'"
                }), status=402)
        product = api.models.Orders.query.filter_by(id=int(data['id'])).first()        
        if product:
            if 'status' in data.keys():
                product.status = data['status']        
                 
            db.session.commit()
            db.session.refresh(product)
            product = api.models.Orders.query.filter_by(id=data['id']).first()
            if product:
                return Response(json.dumps({
                    'Message': "Successfully updated"
                }), status=200)
        else: 
            return Response(json.dumps({"Error":'Order not found'}),status=400)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)

@orders_controller.route('/v1/order/pay', methods=['POST'])
def pay():
    try:
        data = json.loads(request.data)
        for key in ['amount','email','currency','source','customer']:
                if key not in data.keys():
                    return Response(json.dumps({
                        'Error': "Missing parameter '" + key + "'"
                    }), status=402)            
                   
        
        intent = stripe.PaymentIntent.create(
            amount=data['amount'],
            currency=data['currency'],
            receipt_email=data['email'],
            payment_method_types=["card"]
                   
        )
        
        cust_id = 'pi_'+str(intent['client_secret']).split('_')[1]
        
        result = stripe.PaymentIntent.confirm(cust_id,payment_method="pm_card_visa")
        
        if result:
            return Response(json.dumps({
                    'Message': "Successfully payment",
                    "client_secret": cust_id
                }), status=200)
        else:
            return Response(json.dumps({
                    'Message': "Failed payment"
                }), status=400)
            
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)