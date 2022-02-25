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
    d = {'http': 'https://hatsu.vincentrps.xyz', 'gateway': 'wss://gateway.vincentrps.xyz', 'available': ['1']}
    return Response(json.dumps(d), 200)

app.before_serving(connect)

bps = {
    channels.channels: '/v1/guilds',
    guilds_core.guilds: '/v1/guilds',
    me.users_me: '/v1/users/@me',
    users_core.users: '/v1/users'
}

for value, suffix in bps.items():
    app.register_blueprint(value, url_prefix=suffix)
