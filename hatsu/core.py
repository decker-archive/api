import json
import dotenv
import logging
import quart_rate_limiter
from quart import Quart, Response
from .rest.guilds import channels, core as guilds_core
from .rest.users import me, core as users_core
from .rest.gateway import connect

app = Quart(__name__)
dotenv.load_dotenv()
logging.basicConfig(level=logging.DEBUG)

rates = quart_rate_limiter.RateLimiter(app=app)

@app.route('/')
async def health_check():
    d = {'http': 'https://hatsu.vincentrps.xyz', 'gateway': 'wss://gateway.vincentrps.xyz'}
    return Response(json.dumps(d), 200)

app.before_serving(connect)

bps = {
    channels.channels: '/guilds',
    guilds_core.guilds: '/guilds',
    me.users_me: '/users/@me',
    users_core.users: '/users'
}

for value, suffix in bps.items():
    app.register_blueprint(value, url_prefix=suffix)
