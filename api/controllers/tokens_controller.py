from flask import Blueprint, request, Response
from flask_cors import CORS
import api.models
from api.helpers.raise_exception import raiseException
import json
from api import db
from flask import jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

tokens_controller = Blueprint('tokens_controller', __name__)
CORS(tokens_controller)

@tokens_controller.route("/v1/list/tokens", methods=['GET'])
def get_tokens():
    try:
        
        tokens = api.models.Tokens.query.all()
        result=[]
        if tokens:
            for data in tokens:
                result.append({
                    'id': data.id,
                    'api-key':data.api_key
                })
        return Response(json.dumps({"data":result}),status=200)
    except Exception as e:
        if e.__class__.__name__ == "IntegrityError":
            db.session.rollback()
        return raiseException(e)


