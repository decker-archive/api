from datetime import timedelta
import quart
from ..database import channels, users
from ..data_bodys import error_bodys
from quart_rate_limiter import rate_limit

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
    d: dict = await quart.request.get_json()
    try:
        data = {
            'name': d['name'],

        }
    except KeyError:
        return quart.Response(error_bodys['invalid_data'], 400)
