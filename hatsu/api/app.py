import json
import dotenv
import logging

from quart import Quart, Response
from .guilds import channels, core as guilds_core
from .users import me, core as users_core
from .gateway import connect
from .rate import rater

app = Quart(__name__)
dotenv.load_dotenv()
app.config['debug'] = True
logging.basicConfig(level=logging.DEBUG)
rater.init_app(app)



@app.route('/api/ping')
async def health_check():
    d = {
        'url': 'wss://gateway.vincentrps.xyz',
    }
    return Response(json.dumps(d), 200)


app.before_serving(connect)

@app.after_request
async def after_request(resp: Response):
    if rater.current_limit:
        resp.headers.add('X-RateLimit-Bucket', rater.current_limit.key)
    
    return resp

bps = {
    channels.channels: '/api/guilds',
    guilds_core.guilds: '/api/guilds',
    me.users_me: '/api/users/@me',
    users_core.users: '/api/users',
}

for value, suffix in bps.items():

    if value.name == 'guilds':
        rater.limit('10/second')(value)
    elif value.name == 'users_me':
        rater.limit('5/second')(value)
    else:
        rater.limit('7/second')(value)

    app.register_blueprint(value, url_prefix=suffix)
