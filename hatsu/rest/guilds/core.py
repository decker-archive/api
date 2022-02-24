import quart
import json

from datetime import timedelta
from quart_rate_limiter import rate_limit
from ..checks import check_session_, check_if_in_guild
from ..data_bodys import error_bodys
from ..database import guilds as guilds_db, channels
from ..snowflakes import snowflake_with_blast

guilds = quart.Blueprint('guilds', __name__)

"""
    mem = check_if_in_guild(d)

    if mem == None:
        return quart.Response(error_bodys['not_in_guild'], 401)
"""

@guilds.post('/')
@rate_limit(1, timedelta(minutes=1))
async def create_guild():
    owner = check_session_(quart.request.headers.get('Authorization'))
    if owner == None:
        return quart.Response(error_bodys['no_auth'], 401)

    d: dict = await quart.request.get_json()
    
    try:
        req = {
            'id': snowflake_with_blast(7),
            'name': d['name'],
            'description': d.get('description', ''),
            'banner': d.get('banner', ''),
            'invite_banner': d.get('invite_banner', ''),
            'vanity_url': None,
            'verified': False,
            'partnered': False,
            'official': False,
            'owner': owner['id'],
            'safety': {
                'level': 0,
                'msg_notifs': False,
            }
        }
    except KeyError:
        return quart.Response(error_bodys['invalid_data'], 400)

    old = req.copy()
    cat_id = snowflake_with_blast(5)
    cat = {
        'id': cat_id,
        'name': 'General',
        'description': 'The first category of your brand new hatsu server!',
        'inside_of': 0,
        'type': 1,
    }
    default_channels = {
        'id': snowflake_with_blast(2),
        'name': 'general',
        'description': 'The first channel of your brand new hatsu server!',
        'type': 2,
        'guild_id': req['id'],
        'inside_of': cat_id,
    }
    guilds_db.insert_one(req)
    channels.insert_many([cat, default_channels])

    return quart.Response(json.dumps(old), 201)
