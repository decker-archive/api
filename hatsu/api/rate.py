import flask_limiter
import quart.flask_patch
from flask_limiter.util import get_remote_address
from quart import request
from dotenv import load_dotenv

load_dotenv()

def get_key_func():
    if request.headers.get('Authorization'):
        return request.headers.get('Authorization')
    else:
        return get_remote_address()

rater = flask_limiter.Limiter(
    default_limits=['10/second', '40/minute'], 
    headers_enabled=True, 
    key_func=get_key_func,
)