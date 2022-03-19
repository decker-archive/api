import ulid
import quart
import json
import datetime
from quart import Blueprint, request
from ..data_bodys import error_bodys
from ..database import users, user_settings

bots = Blueprint('bots-v3', __name__)


@bots.post('')
async def create_bot():
    auth = request.headers.get('Authorization', '')

    user = users.find_one({'session_ids': [auth]}) 

    if user == None:
        return quart.Response(error_bodys['no_auth'], 401)

    if user['bot']:
        return quart.Response(error_bodys['no_perms'], 403)

    d: dict = await quart.request.get_json()

    if not isinstance(d['separator'], str):
        return quart.Response(error_bodys['invalid_data'], status=400)

    if len(d['separator']) != 4:
        return quart.Response(body=error_bodys['invalid_data'], status=400)

    if d['separator'] == '0000':
        return quart.Response(error_bodys['invalid_data'], status=400)
    
    em = users.find_one({'email': d.get('email')})

    if em != None:
        return quart.Response(error_bodys['invalid_data'], status=400)

    _id = ulid.new().str

    try:
        given = {
            '_id': _id,
            'username': d['username'],
            'separator': d['separator'],
            'bio': d.get('bio', ''),
            'avatar_url': None,
            'banner_url': None,
            'flags': 1 >> 2,
            'system': False,
            'email_verified': True,
            'session_ids': [ulid.new().hex],
            'blocked_users': [],
            'bot': True,
            'created_at': datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
    except KeyError:
        return quart.Response(body=error_bodys['invalid_data'], status=400)
    else:
        r = quart.Response(json.dumps(given), status=201)
        await user_settings.insert_one({'_id': _id, 'accept_friend_requests': False})
        await users.insert_one(given)
        return r
