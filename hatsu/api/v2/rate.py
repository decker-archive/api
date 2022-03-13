import asyncio
from typing import Dict
import flask_limiter
import quart.flask_patch
from quart import request, abort
from dotenv import load_dotenv
from .snowflakes import snowflake_with_blast

load_dotenv()

keys: Dict[str, str] = {}

def get_key_func():
    try:
        compat = request.method + ':' + request.endpoint + ':' + request.remote_addr
    except:
        abort(404)
    for k, v in keys.items():
        if k == compat:
            return v

    id = snowflake_with_blast()
    keys[compat] = id
    return id

async def _reset():
    await asyncio.sleep(4000)
    keys.clear()
    await _reset()

rater = flask_limiter.Limiter(
    default_limits=['5/second', '50/minute', '10000/hour'],
    headers_enabled=False,
    key_func=get_key_func,
    retry_after='delta-seconds',
    key_prefix=snowflake_with_blast(),
)
