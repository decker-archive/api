import quart
import json

from datetime import timedelta, datetime, timezone
from quart_rate_limiter import rate_limit
from ..checks import check_session_, check_if_in_guild
from ..data_bodys import error_bodys
from ..database import guilds as guilds_db, channels, members, guild_invites
from ..snowflakes import snowflake_with_blast
from ..gateway import dispatch_event_to

guilds = quart.Blueprint('guilds', __name__)

"""
    mem = check_if_in_guild(d)

    if mem == None:
        return quart.Response(error_bodys['not_in_guild'], 403)
"""


@guilds.post('')
@rate_limit(1, timedelta(minutes=1))
async def create_guild():
    owner = check_session_(quart.request.headers.get('Authorization'))
    if owner == None:
        return quart.Response(error_bodys['no_auth'], 401)

    d: dict = await quart.request.get_json()
    id = snowflake_with_blast(7)

    try:
        req = {
            'id': id,
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
            },
            'emojis': [],
            'roles': [{
                'id': 0,
                'name': 'everyone',
                'position': 0,
                'color': '#000000',
                'permissions': [
                    'VIEW_CHANNELS',
                    'READ_MESSAGES',
                    'SEND_MESSAGES'
                ]
            }]
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
        },
        'nick': None,
        'avatar_url': None,
        'banner_url': None,
        'joined_at': datetime.now(timezone.utc).isoformat(),
        'deaf': False,
        'mute': False,
        'owner': True,
        'guild_id': id,
        'roles': [0]
    }
    members.insert_one(first_joined)
    guilds_db.insert_one(req)
    channels.insert_many([cat, default_channels])

    await dispatch_event_to(owner['id'], 'GUILD_CREATE', old)

    return quart.Response(json.dumps(old), 201)

@guilds.get('/<int:guild_id>')
@rate_limit(5, timedelta(seconds=1))
async def get_guild(guild_id):
    user = check_session_(quart.request.headers.get('Authorization'))
    if user == None:
        return quart.Response(error_bodys['no_auth'], 401)
    
    member = members.find_one(user['id'])

    if member == None:
        return quart.Response(error_bodys['no_auth'], 401)
    
    guild = guilds_db.find_one({'id': guild_id})

    if guild == None:
        return quart.Response(error_bodys['not_found'], 404)
    
    return quart.Response(json.dumps(guild), 200)

@guilds.get('/<int:guild_id>/members')
@rate_limit(10, timedelta(minutes=1))
async def get_guild_members(guild_id):
    user = check_session_(quart.request.headers.get('Authorization'))
    if user == None:
        return quart.Response(error_bodys['no_auth'], 401)
    
    objs = members.find({'guild_id': guild_id})

    ret = []

    for _obj in objs:
        _obj.pop('guild_id')
        ret.append(_obj)
    
    return quart.Response(json.dumps(ret), 200)

@guilds.post('/invites/<int:invite_str>')
@rate_limit(5, timedelta(seconds=1))
async def join_guild(invite_str):

    user = check_session_(quart.request.headers.get('Authorization'))
    
    if user == None:
        return quart.Response(error_bodys['no_auth'], 401)

    invite = guild_invites.find_one({'code': invite_str})

    if invite == None:
        return quart.Response(error_bodys['not_found'], 404)
    
    c = members.find_one({'guild_id': invite['guild_id'], 'id': user['id']})

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
        },
        'nick': None,
        'avatar_url': None,
        'banner_url': None,
        'joined_at': datetime.now(timezone.utc).isoformat(),
        'deaf': False,
        'mute': False,
        'permissions': [],
        'guild_id': id,
        'roles': [0]
    }
    ret = member.copy()
    ret.pop('guild_id')
    members.insert_one(member)

    return quart.Response(json.dumps(ret), 200)

@guilds.get('/<int:guild_id>/preview')
@rate_limit(1, timedelta(seconds=1))
async def get_guild_preview(guild_id):

    guild = guilds_db.find_one({'id': guild_id})

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
