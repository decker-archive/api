import quart
import json

from datetime import timedelta, datetime, timezone
from ..checks import check_session_
from ..data_bodys import error_bodys
from ..database import guilds as guilds_db, channels, members, guild_invites
from ..snowflakes import snowflake_with_blast, invite_code
from ..gateway import dispatch_event_to, guild_dispatch

guilds = quart.Blueprint('guilds', __name__)

"""
    mem = await check_if_in_guild(d)

    if mem == None:
        return quart.Response(error_bodys['not_in_guild'], 403)
"""


@guilds.post('')
async def create_guild():
    owner = await check_session_(quart.request.headers.get('Authorization'))
    if owner == None:
        return quart.Response(error_bodys['no_auth'], 401)

    d: dict = await quart.request.get_json()
    id = snowflake_with_blast()

    try:
        req = {
            'id': id,
            'name': d['name'],
            'description': d.get('description', ''),
            'banner': None,
            'invite_banner': None,
            'vanity_url': None,
            'verified': False,
            'partnered': False,
            'official': False,
            'owner': owner['id'],
            'emojis': [],
            'roles': [
                {
                    'id': 0,
                    'name': 'everyone',
                    'position': 0,
                    'color': '#000000',
                    'permissions': [
                        'VIEW_CHANNELS',
                        'READ_MESSAGES',
                        'SEND_MESSAGES',
                        'CREATE_INVITES',
                    ],
                }
            ],
        }
    except KeyError:
        return quart.Response(error_bodys['invalid_data'], 400)

    old = req.copy()
    cat_id = snowflake_with_blast()
    cat = {
        'id': cat_id,
        'name': 'General',
        'description': 'The first category of your brand new hatsu server!',
        'inside_of': 0,
        'type': 1,
        'position': 0,
        'guild_id': req['id'],
    }
    default_channels = {
        'id': snowflake_with_blast(),
        'name': 'general',
        'description': 'The first channel of your brand new hatsu server!',
        'type': 2,
        'guild_id': req['id'],
        'inside_of': cat_id,
        'position': 0,
    }
    first_joined = {
        'user': {
            'id': owner['id'],
            'username': owner['username'],
            'separator': owner['separator'],
            'avatar_url': owner['avatar_url'],
            'banner_url': owner['banner_url'],
            'flags': owner['flags'],
            'verified': owner['verified'],
            'system': owner['system'],
            'session_ids': owner['session_ids'],
        },
        'nick': None,
        'avatar_url': None,
        'banner_url': None,
        'joined_at': datetime.now(timezone.utc).isoformat(),
        'deaf': False,
        'mute': False,
        'owner': True,
        'guild_id': id,
        'roles': [0],
    }
    await members.insert_one(first_joined)
    await guilds_db.insert_one(req)
    await channels.insert_many([cat, default_channels])

    await dispatch_event_to(owner['id'], 'GUILD_CREATE', old)

    return quart.Response(json.dumps(old), 201)


@guilds.patch('/<int:guild_id>')
async def edit_guild(guild_id: int):
    user = await check_session_(quart.request.headers.get('Authorization'))
    if user == None:
        return quart.Response(error_bodys['no_auth'], 401)

    member = await members.find_one(user['id'])

    if member == None:
        return quart.Response(error_bodys['no_auth'], 401)

    guild = await guilds_db.find_one({'id': guild_id})

    if guild == None:
        return quart.Response(error_bodys['not_found'], 404)

    allow = False

    for perm in member['roles'][0]['permissions']:
        if perm == 'MANAGE_GUILD':
            allow = True

    # incorrect permissions
    if allow == False:
        return quart.Response(error_bodys['no_perms'], 403)

    json: dict = await quart.request.get_json()

    data = {}

    if json.get('name'):
        data['name'] = json.pop('name')

    if json.get('description'):
        data['description'] = json.pop('name')

    d = data.copy()

    await guilds_db.update_one({'id': guild_id}, data)

    await guild_dispatch(guild['id'], 'GUILD_UPDATE', d)

    return quart.Response(d, 200)


@guilds.delete('/<int:guild_id>')
async def delete_guild(guild_id: int):
    user = await check_session_(quart.request.headers.get('Authorization'))
    if user == None:
        return quart.Response(error_bodys['no_auth'], 401)

    member = await members.find_one(user['id'])

    if member == None:
        return quart.Response(error_bodys['no_auth'], 401)

    guild = await guilds_db.find_one({'id': guild_id})

    if guild == None:
        return quart.Response(error_bodys['not_found'], 404)

    if member['owner'] is False:
        return quart.Response(error_bodys['no_perms'], 403)

    await guilds_db.delete_one({'id': guild_id})
    await members.delete_many({'guild_id': guild_id})
    await channels.delete_many({'guild_id': guild_id})

    await guild_dispatch(guild['id'], 'GUILD_DELETE', None)

    return quart.Response(error_bodys['no_content'], 204)


@guilds.get('/<int:guild_id>')
async def get_guild(guild_id):
    user = await check_session_(quart.request.headers.get('Authorization'))
    if user == None:
        return quart.Response(error_bodys['no_auth'], 401)

    member = await members.find_one(user['id'])

    if member == None:
        return quart.Response(error_bodys['no_auth'], 401)

    guild = await guilds_db.find_one({'id': guild_id})

    if guild == None:
        return quart.Response(error_bodys['not_found'], 404)

    return quart.Response(json.dumps(guild), 200)


@guilds.get('/<int:guild_id>/members')
async def get_guild_members(guild_id):
    user = await check_session_(quart.request.headers.get('Authorization'))
    if user == None:
        return quart.Response(error_bodys['no_auth'], 401)

    objs = members.find({'guild_id': guild_id})

    ret = []

    for _obj in objs:
        _obj.pop('guild_id')
        _obj['user'].pop('session_ids')
        ret.append(_obj)

    return quart.Response(json.dumps(ret), 200)


@guilds.post('/invites/<int:invite_str>')
async def join_guild(invite_str):

    user = await check_session_(quart.request.headers.get('Authorization'))

    if user == None:
        return quart.Response(error_bodys['no_auth'], 401)

    invite = await guild_invites.find_one({'code': invite_str})

    if invite == None:
        return quart.Response(error_bodys['not_found'], 404)

    c = await members.find_one({'guild_id': invite['guild_id'], 'id': user['id']})

    if c != None:
        return quart.Response(error_bodys['already_in_guild'], 409)

    member = {
        'user': {
            'id': user['id'],
            'username': user['username'],
            'separator': user['separator'],
            'avatar_url': user['avatar_url'],
            'banner_url': user['banner_url'],
            'flags': user['flags'],
            'verified': user['verified'],
            'system': user['system'],
            'session_ids': user['session_ids'],
        },
        'nick': None,
        'avatar_url': None,
        'banner_url': None,
        'joined_at': datetime.now(timezone.utc).isoformat(),
        'deaf': False,
        'mute': False,
        'permissions': [],
        'guild_id': id,
        'roles': [0],
    }
    ret = member.copy()
    ret.pop('guild_id')
    ret['user'].pop('session_ids')
    dis = member.copy()
    dis.pop('guild_id')
    dis['user'].pop('session_ids')
    await members.insert_one(member)

    await guild_dispatch(
        invite['guild_id'],
        'MEMBER_JOIN',
        {'member': dis, 'guild_id': invite['guild_id']},
    )

    return quart.Response(json.dumps(ret), 200)


@guilds.get('/<int:guild_id>/preview')
async def get_guild_preview(guild_id):

    guild = await guilds_db.find_one({'id': guild_id})

    if guild == None:
        return quart.Response(error_bodys['not_found'], 404)

    ret = {
        'name': guild['name'],
        'description': guild['description'],
        'invite_banner': guild['invite_banner'],
        'partnered': guild['partnered'],
        'official': guild['official'],
        'emojis': guild['emojis'],
    }

    return quart.Response(json.dumps(ret), 200)


@guilds.post('/<int:guild_id>/invites')
async def create_invite(guild_id):
    user = await check_session_(quart.request.headers.get('Authorization'))

    if user == None:
        return quart.Response(error_bodys['no_auth'], 401)

    c = await members.find_one({'guild_id': guild_id, 'id': user['id']})

    if c == None:
        return quart.Response(error_bodys['not_in_guild'], 403)

    top_role = await guilds_db.find_one(c['roles'][0])

    allow = False

    for perm in top_role['permissions']:
        if perm == 'CREATE_INVITES':
            allow = True

    if allow == False:
        return quart.Response(error_bodys['no_auth'], 401)

    code = await invite_code()

    await guild_invites.insert_one({'guild_id': guild_id, 'code': code})

    await guild_dispatch(
        guild_id, 'INVITE_CREATE', {'code': code, 'guild_id': guild_id}
    )

    return quart.Response(json.dumps({'code': code}), 201)
