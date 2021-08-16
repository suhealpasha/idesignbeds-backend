from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_apscheduler import APScheduler
import time
import datetime

app = Flask(__name__)

app.config.from_object(Config())
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
db = SQLAlchemy(app)


CORS(app)

from .policies.api_key_validator import api_key_validation_policy
from .policies.request_header_validator import request_header_validation_policy
from .controllers.customer_controller import customer_controller
from .controllers.tokens_controller import tokens_controller
from .controllers.admin_controller import admin_controller
from .controllers.products_controller import products_controller
from .controllers.categories_controller import categories_controller
from .controllers.colors_controller import colors_controller
from .controllers.addons_controller import addons_controller
from .controllers.main_categories_controller import main_categories_controller
from .controllers.reviews_controller import reviews_controller
from .controllers.baskets_controller import baskets_controller
from .controllers.orders_controller import orders_controller

app.register_blueprint(request_header_validation_policy)
app.register_blueprint(api_key_validation_policy)
app.register_blueprint(tokens_controller)
app.register_blueprint(admin_controller)
app.register_blueprint(products_controller)
app.register_blueprint(categories_controller)
app.register_blueprint(colors_controller)
app.register_blueprint(addons_controller)
app.register_blueprint(main_categories_controller)
app.register_blueprint(reviews_controller)
app.register_blueprint(customer_controller)
app.register_blueprint(baskets_controller)
app.register_blueprint(orders_controller)

# db.drop_all()
# db.create_all()


scheduler = APScheduler()
Config.JOBS=[
    
]
app.config.from_object(Config())

scheduler.init_app(app)
scheduler.start()