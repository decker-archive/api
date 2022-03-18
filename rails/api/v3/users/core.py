import quart
import json
from ..database import users as users_db
from ..data_bodys import error_bodys
from ..checks import check_session_

users = quart.Blueprint('users-v3', __name__)


@users.get('/<int:user_id>')
async def get_user(user_id: int):
    d = await check_session_(quart.request.headers.get('Authorization'))

    if d == None:
        return quart.Response(error_bodys['no_auth'], 401)

    user = users_db.find_one({'_id': user_id})

    if user == None:
        return quart.Response(error_bodys['not_found'], 404)

    # filter out non-public info, like session_ids
    user_data = {
        '_id': user['_id'],
        'username': user['username'],
        'separator': user['separator'],
        'bio': user['bio'],
        'avatar_url': user['avatar_url'],
        'banner_url': user['banner_url'],
        'flags': user['flags'],
        'verified': user['verified'],
        'system': user['system'],
    }

    return quart.Response(json.dumps(user_data), 200)
