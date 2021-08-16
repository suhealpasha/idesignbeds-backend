from flask import Blueprint, request, Response
from flask_cors import CORS
import json
import api.models

api_key_validation_policy = Blueprint('api_key_validation_policy', __name__)
CORS(api_key_validation_policy)

@api_key_validation_policy.before_app_request
def validate_api_key(*args, **kwargs):
    try:
        if request.endpoint not in ["health_check","orders_controller.pay","orders_controller.delete_order","orders_controller.update_order","orders_controller.list_orders","reviews_controller.review_by_customer","orders_controller.get_orders_by_customer","orders_controller.register","baskets_controller.delete_all_basket","baskets_controller.delete_basket","baskets_controller.get_baskets_by_customer","baskets_controller.register","reviews_controller.review_by_product","products_controller.product_details","products_controller.get_cat_products","main_categories_controller.image_upload","customer_controller.delete_customer","customer_controller.get_allcustomers","customer_controller.customer_exist","customer_controller.register","customer_controller.edit","customer_controller.login","customer_controller.customer_details","reviews_controller.delete_review","reviews_controller.get_reviews","reviews_controller.register","reviews_controller.profile_upload","main_categories_controller.delete_main_category","main_categories_controller.register","main_categories_controller.get_main_categories","addons_controller.register","addons_controller.get_addons","addons_controller.delete_addon","categories_controller.delete_category","colors_controller.delete_color","colors_controller.get_colors","colors_controller.register","categories_controller.register","categories_controller.get_categories","products_controller.display_image","products_controller.get_products","products_controller.register","products_controller.update_product","products_controller.upload","admin_controller.login","admin_controller.forgot_password","admin_controller.reset_password","tokens_controller.get_tokens","admin_controller.register"]:
            data = request.headers
            if not 'api_key' in data:
                return Response(json.dumps({
                    'Error': "Missing header 'api_key'"
                }), status=401)
            device = api.models.Tokens.query.filter_by(api_key=data['api_key']).first()
            
            if not device:
                return Response(json.dumps({
                    'Error': "Unknown API Key"
                }), status=401)
    except Exception as exception:
        return Response(json.dumps({
            str(exception.__class__.__name__): str(exception)
        }), status=500) 
        