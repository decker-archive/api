import json
import dotenv
import logging
import hypercorn.asyncio
import hypercorn.config
import quart.flask_patch

from quart import Quart, Response
from .guilds import channels, core as guilds_core
from .users import me, core as users_core
from .gateway import connect
from .rate import rater
from .database import loop
from .ui import friends

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

@app.after_request
async def after_request(resp: Response):
    if rater.current_limit:
        resp.headers.add('X-RateLimit-Bucket', rater.current_limit.key)
    return resp

bps = {
    channels.channels: '/api/guilds',
    guilds_core.guilds: '/api/guilds',
    me.users_me: '/api/users/@me',
    users_core.users: '/users',
    friends.ui: '/api/ui/friends',
}

for value, suffix in bps.items():
    app.register_blueprint(value, url_prefix=suffix)

cfg = hypercorn.config.Config()
cfg.bind.clear()
cfg.bind.append('localhost:1111')

loop.create_task(connect())
loop.run_until_complete(hypercorn.asyncio.serve(app, cfg))
loop.run_forever()
