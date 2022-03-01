import json
import dotenv
import logging
import quart.flask_patch

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



@app.route('/gateway')
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
    channels.channels: '/guilds',
    guilds_core.guilds: '/guilds',
    me.users_me: '/users/@me',
    users_core.users: '/users',
}

for value, suffix in bps.items():
    app.register_blueprint(value, url_prefix=suffix)
