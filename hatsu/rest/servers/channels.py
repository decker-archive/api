from datetime import timedelta
import quart
from ..database import channels, users, members
from ..data_bodys import error_bodys
from quart_rate_limiter import rate_limit
from ..snowflakes import snowflake_with_blast
from ..gateway import dispatch_event

@rate_limit(20, period=timedelta(minutes=1))
async def create_channel():
    auth = quart.request.headers.get('Authorization')
    ver = users.find_one({'session_ids': [auth]})
    let = False

    for session_id in ver['session_ids']:
        if session_id == auth:
            let = True
    
    if let == False:
        return quart.Response(error_bodys['no_auth'], 401)

    member  = members.find_one({'id': ver['id']})

    if member == None:
        return quart.Response(error_bodys['not_in_server'], 401)
    
    d: dict = await quart.request.get_json()

    if d.get('type') not in (1):
        return quart.Response(error_bodys['invalid_data'], 400)

    try:
        data = {
            'id': snowflake_with_blast(2),
            'name': d['name'],
            'server_id': d['server_id'],
            'type': d['type']
        }
    except KeyError:
        return quart.Response(error_bodys['invalid_data'], 400)
    
    await dispatch_event('channel_create', data)
