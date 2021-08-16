# Define the application directory
import os
from sqlalchemy import create_engine
from sshtunnel import SSHTunnelForwarder
import sshtunnel
import mysql.connector
import logging 

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
# THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
# CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
# CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
# SECRET_KEY = "secret"


class Config(object):
    DEBUG = True
    ENV = 'development'
    APP_MYSQL_DATABASE = 'idesignbeds'
    APP_MYSQL_PASSWORD = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    user = 'root'
    password = ''
    host = '127.0.0.1'
    port = '3306'
    APP_MYSQL_DATABASE = 'idesignbeds'
            
    
  
   
    SQLALCHEMY_DATABASE_URI = 'mysql://b57c0919726415:6f64ab19@us-cdbr-east-04.cleardb.com/heroku_d571709bdd12a6c' 
    # 'mysql+pymysql://root:root123@127.0.0.1:3306/idesignbeds' 
    
   