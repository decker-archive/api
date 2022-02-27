import json
import os
import dotenv
import logging
import quart.flask_patch # type: ignore
import flask_limiter
from flask_limiter.util import get_remote_address

from quart import Quart, Response, request
from .guilds import channels, core as guilds_core
from .users import me, core as users_core
from .gateway import connect

app = Quart(__name__)
dotenv.load_dotenv()
app.config['debug'] = True
logging.basicConfig(level=logging.DEBUG)

def get_key_func():
    if request.headers.get('Authorization'):
        return request.headers.get('Authorization')
    else:
        return get_remote_address()

rater = flask_limiter.Limiter(
    app, 
    default_limits=['4/second', '40/minute'], 
    headers_enabled=True, 
    storage_uri=os.getenv('mongo_uri'),
    key_func=get_key_func,
)

@app.route('/')
async def health_check():
    d = {
        'gateway': 'wss://gateway.vincentrps.xyz',
        'available': ['1'],
    }
    return Response(json.dumps(d), 200)


app.before_serving(connect)

@app.after_request
async def after_request(resp: Response):
    if rater.current_limit:
        resp.headers.add('X-RateLimit-Bucket', rater.current_limit.key)
    
    return resp

bps = {

    # api v1
    channels.channels: '/api/v1/guilds',
    guilds_core.guilds: '/api/v1/guilds',
    me.users_me: '/api/v1/users/@me',
    users_core.users: '/api/v1/users',

    # api v2    
    channels.channels: '/api/v2/guilds',
    guilds_core.guilds: '/api/v2/guilds',
    me.users_me: '/api/v2/users/@me',
    users_core.users: '/api/v2/users',
}

for value, suffix in bps.items():

    if value.name == 'guilds':
        rater.limit('10/second')(value)
    elif value.name == 'users_me':
        rater.limit('5/second')(value)
    else:
        rater.limit('7/second')(value)

    app.register_blueprint(value, url_prefix=suffix)
