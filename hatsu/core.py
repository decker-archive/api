import json
import dotenv
import logging
import os
import hypercorn.asyncio
import hypercorn.config
import quart.flask_patch

from quart import Quart, Response
from .api.v2.guilds import channels, core as guilds_core
from .api.v2.users import me, core as users_core
from .api.gateway import connect
from .api.v2.rate import rater
from .api.v2.database import loop
from .api.v2.ui import friends

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

@app.errorhandler(404)
async def not_found():
    return json.dumps({'code': 0, 'message': '404: Not Found'})

@app.errorhandler(500)
async def internal():
    return json.dumps({'code': 0, 'message': '500: Internal Server Error'})

bps = {
    channels.channels: '/v2/guilds',
    guilds_core.guilds: '/v2/guilds',
    me.users_me: '/v2/users/@me',
    users_core.users: '/v2/users',
    friends.ui: '/v2/ui/friends',
}

for value, suffix in bps.items():
    app.register_blueprint(value, url_prefix=suffix)

cfg = hypercorn.config.Config()
cfg.bind.clear()
cfg.bind.append(f'0.0.0.0:{os.getenv("PORT")}')

loop.create_task(connect())
loop.run_until_complete(hypercorn.asyncio.serve(app, cfg))
loop.run_forever()
