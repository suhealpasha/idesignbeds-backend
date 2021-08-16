from flask import Blueprint, request
from flask_cors import CORS

request_header_validation_policy = Blueprint(
    'request_header_validation_policy', __name__)
CORS(request_header_validation_policy)


@request_header_validation_policy.before_app_request
def validate_request_header(*args, **kwargs):
    if request.method == 'OPTIONS':
        headers = {
            'Content-type':'multipart/form-data,application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PUT, DELETE',
            'Access-Control-Max-Age': 1000,
            'Access-Control-Allow-Headers': 'origin, x-csrftoken, content-type, accept, x-api-key, session_key, authorization',
        }
        return '', 200, headers
        