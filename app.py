# ************************************************************************** #
# Flask REST API to run Security Centric
# ************************************************************************** #

# ########################################################################## #
# Includes
# ########################################################################## #
from api import app
import json
from flask import Response
import datetime
import schedule
from threading import Timer
import time
import bottle
from flask import jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024 # (or whatever you want)
# ########################################################################## #
# Globals
# ########################################################################## #

# ########################################################################## #
# Methods
# ########################################################################## #

# ########################################################################## #
# Flask Stuff
# ########################################################################## #

app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config["JWT_SECRET_KEY"] = "super-secret"
UPLOAD_FOLDER = 'api/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app._static_folder = UPLOAD_FOLDER
jwt = JWTManager(app)
@app.route("/", methods=['GET'])

def health_check():
    
    return Response(json.dumps({
        'message': 'OK',
        'time': str(datetime.datetime.utcnow())
    }), status=200)



# ######################################################################### #
# Main
# ########################################################################## #



        
           
if __name__ == '__main__':
    
    app.run(host='127.0.0.1', port=5000)
    