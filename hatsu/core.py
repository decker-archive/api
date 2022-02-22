import json
import websockets.server
import dotenv
import quart_rate_limiter
import logging
from quart import Quart, Response
from .gateway import handler
from .rest.servers import channels
from .rest.users import create_user, get_me, edit_user

app = Quart(__name__)
dotenv.load_dotenv()
logging.basicConfig(level=logging.DEBUG)

rates = quart_rate_limiter.RateLimiter(app=app)

# users
app.add_url_rule('/v1/users/@me', view_func=create_user, methods=['POST'])
app.add_url_rule('/v1/users/@me', view_func=get_me, methods=['GET'])
app.add_url_rule('/v1/users/@me', view_func=edit_user, methods=['PATCH'])

app.sessions = set()

async def start_websocket():
    
    async def _wrapper(ws, url):
        await handler.gateway_handler(app, ws, url)

    kwargs = {'ws_handler': _wrapper, 'host': '0.0.0.0', 'port': 443}

    return websockets.server.serve(**kwargs)

@app.route('/')
async def health_check():
    d = {'success': True, 'message': 'Welcome'}
    return Response(json.dumps(d), 200)

@app.before_serving
async def app_before_serving():
    ...
