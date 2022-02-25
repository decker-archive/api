import json
import quart
from datetime import timedelta
from ..snowflakes import snowflake_with_blast
from ..data_bodys import error_bodys
from ..database import users
from ..encrypt import get_hash_for
from quart_rate_limiter import rate_limit

users_me = quart.Blueprint('users_me', __name__)


@users_me.post('/')
@rate_limit(1, timedelta(hours=1))
async def create_user():
    d: dict = await quart.request.get_json()

    if d['separator'] == int:
        return quart.Response(error_bodys['invalid_data'], status=400)

    if len(d['separator']) != 4:
        return quart.Response(body=error_bodys['invalid_data'], status=400)

    if d['separator'] == 0000:
        return quart.Response(error_bodys['invalid_data'], status=400)

    try:
        given = {
            'id': snowflake_with_blast(0),
            'username': d['username'],
            'separator': d['separator'],
            'bio': d.get('bio', ''),
            'avatar_url': None,
            'banner_url': None,
            'flags': ['Early Adopter'],
            'verified': False,
            'email': d['email'],
            'password': get_hash_for(d.pop('password')),
            'system': False,
            'email_verified': False,
            'session_ids': [str(snowflake_with_blast(7))],
        }
    except KeyError:
        return quart.Response(body=error_bodys['invalid_data'], status=400)
    else:
        r = quart.Response(json.dumps(given), status=201)
        users.insert_one(given)
        return r


@users_me.patch('/')
@rate_limit(2, timedelta(seconds=1))
async def edit_user():
    auth = quart.request.headers.get('Authorization', '')
    allow = False
    for session_id in users.find({'session_ids': [auth]}):
        if session_id == quart.request.headers.get('Authorization'):
            allow = True

    if allow == False:
        return quart.Response(error_bodys['no_auth'], status=401)

    d: dict = await quart.request.get_json()

    if d.get('separator'):
        if len(d['separator']) != 4:
            return quart.Response(error_bodys['invalid_data'], 400)
        elif d['separator'] == 0000:
            return quart.Response(error_bodys['invalid_data'], 400)

    given = {}

    if d.get('username'):
        given['username'] = d.pop('username')

    if d.get('separator'):
        given['separator'] = d.pop('sparator')

    if d.get('email'):
        given['email'] = d.pop('email')

    if d.get('password'):
        given['password'] = get_hash_for(d.pop('password'))
    
    if d.get('bio'):
        given['bio'] = d.pop('bio')

    if given == {}:
        return quart.Response(error_bodys['invalid_data'], 400)

    up = users.find_one({'session_ids': [auth]})
    users.update_one(up['id'], given)

    return quart.Response(json.loads(given), 200)


@users_me.get('/')
@rate_limit(5, period=timedelta(seconds=1))
async def get_me():
    auth = quart.request.headers.get('Authorization')
    cur = None
    find = users.find_one({'session_ids': [auth]})

    try:
        for session_id in find['session_ids']:
            if session_id == quart.request.headers.get('Authorization'):
                cur = {
                    'id': find['id'],
                    'username': find['username'],
                    'separator': find['separator'],
                    'bio': find['bio'],
                    'avatar_url': find['avatar_url'],
                    'banner_url': find['banner_url'],
                    'flags': find['flags'],
                    'verified': find['verified'],
                    'system': find['system'],
                }
    except TypeError:
        return quart.Response(error_bodys['no_auth'], status=401)

    if cur is None:
        return quart.Response(error_bodys['no_auth'], status=401)

    return quart.Response(json.dumps(cur))


@users_me.post('/sessions')
@rate_limit(1, timedelta(minutes=30))
async def create_session():
    login: dict = await quart.request.get_json(True)

    u = users.find_one(
        {
            'email': login.get('email', ''),
            'password': get_hash_for(login.get('password', 'nan')),
        }
    )

    if u == None:
        return quart.Response(error_bodys['no_auth'], status=401)

    session_id = snowflake_with_blast(2)

    users.find_one_and_update(
        {
            'email': login.get('email'),
            'password': get_hash_for(login.get('password', 'nan')),
        },
        {'session_ids': [session_id]},
    )
    return quart.Response(json.dumps({'session_id': session_id}), 201)


@users_me.delete('/sessions/<int:session_id>')
@rate_limit(1, timedelta(seconds=1))
async def delete_session(session_id: int):
    login: dict = await quart.request.get_json(True)

    u = users.find_one(
        {
            'email': login.get('email', ''),
            'password': get_hash_for(login.get('password', 'nan')),
        }
    )

    if u == None:
        return quart.Response(error_bodys['no_auth'], status=401)

    users.replace_one({'session_ids': [session_id]}, {'session_ids': []})
    return quart.Response(json.dumps({'completed': True}), 410)
