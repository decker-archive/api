import json
from quart import Blueprint, request, Response
from ..checks import check_session_
from ..data_bodys import error_bodys
from ..database import friends, users, user_settings
from .notifs import send_friend_notification

ui = Blueprint('ui-friends-v3', __name__)

@ui.get('')
async def get_friends():
    user = await check_session_(request.headers.get('Authorization'))

    if user == None:
        return Response(error_bodys['no_auth'], 401)

    _r = friends.find({'_id': user['_id'], 'request': False})

    r = []

    async for f in _r:
        r.append(f['other'])

    return Response(json.dumps(r), 200)

@ui.get('/<int:user_id>')
async def add_friend(user_id: int):
    user = await check_session_(request.headers.get('Authorization'))

    if user == None:
        return Response(error_bodys['no_auth'], 401)
    
    to = await users.find_one({'_id': user_id})

    if to == None:
        return Response(error_bodys['not_found'], 404)

    settings = await user_settings.find_one({'_id': to['_id']})

    if settings['accept_friend_requests'] is False:
        return Response(error_bodys['no_perms'], 403)

    await friends.insert_one({'_id': user['_id'], 'other': user_id, 'request': True})

    await send_friend_notification(user['_id'], user_id, True)

    return Response(error_bodys['no_content'], 204)

@ui.get('/<int:user_id>')
async def remove_friend(user_id: int):
    user = await check_session_(request.headers.get('Authorization'))

    if user == None:
        return Response(error_bodys['no_auth'], 401)
    
    to = await users.find_one({'_id': user_id})

    if to == None:
        return Response(error_bodys['not_found'], 404)

    await friends.delete_one({'_id': user['_id'], 'other': user_id})

    await send_friend_notification(user['_id'], user_id, False)

    return Response(error_bodys['no_content'], 204)
