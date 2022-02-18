"""
hatsu - The okemia rest and gateway api
Copyright (C) 2021-2022, okemia

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import json
import orjson
import sanic
from .snowflakes import snowflake_with_blast
from .data_bodys import error_bodys
from .database import users
from .encrypt import get_hash_for, valid_session_id
from .ratelimiting import ratelimiter

@ratelimiter.limit('1/hour', key_func=valid_session_id)
async def create_user(require: sanic.Request):
    d: dict = require.load_json(loads=orjson.loads)

    if d['separator'] == int:
        return sanic.json(body=error_bodys['invalid_data'], status=400)

    if len(d['separator']) != 4:
        return sanic.json(body=error_bodys['invalid_data'], status=400)
    
    if d['separator'] == 0000:
        return sanic.json(body=error_bodys['invalid_data'], status=400)

    try:
        given = {
            'id': snowflake_with_blast(0),
            'username': d['username'],
            'separator': d['separator'],
            'avatar_url': None,
            'banner_url': None,
            'flags': [
                'Early Adopter'
            ],
            'verified': False,
            'email': d['email'],
            'password': get_hash_for(d.pop('password')),
            'system': False,
            'session_ids': [
                snowflake_with_blast(7)
            ]
        }
    except KeyError:
        return sanic.json(body=error_bodys['invalid_data'], status=400)
    else:
        r = sanic.json(json.dumps(given), status=201)
        users.insert_one(given)
        return r

@ratelimiter.limit('10/minute', key_func=valid_session_id)
async def edit_user(require: sanic.Request):
    auth = require.headers.get('Authorization')
    allow = False
    for session_id in users.find({'session_ids': [auth]}):
        if session_id == require.headers.get('Authorization'):
            allow = True
    
    if allow == False:
        return sanic.json(body=error_bodys['no_auth'], status=401)

    d: dict = require.load_json(loads=orjson.loads)

    if d.get('separator'):
        if len(d['separator']) != 4:
            return sanic.json(body=error_bodys['invalid_data'])
        elif d['separator'] == 0000:
            return sanic.json(body=error_bodys['invalid_data'])
    
    given = {}

    if d.get('username'):
        given['username'] = d.pop('username')
    
    if d.get('separator'):
        given['separator'] = d.pop('sparator')
    
    if d.get('email'):
        given['email'] = d.pop('email')
    
    if d.get('password'):
        given['password'] = get_hash_for(d.pop('password'))
    
    if given == {}:
        return sanic.json(body=error_bodys['invalid_data'])
    
    users.find_one_and_update()

@ratelimiter.limit('100/minute', key_func=valid_session_id)
async def get_me(require: sanic.Request):
    auth = require.headers.get('Authorization')
    cur = None
    find = users.find_one({'session_ids': [auth]})
    
    for session_id in find['session_ids']:
        if session_id == require.headers.get('Authorization'):
            cur = {
            'id': find['id'],
            'username': find['username'],
            'separator': find['separator'],
            'avatar_url': find['avatar_url'],
            'banner_url': find['banner_url'],
            'flags': find['flags'],
            'uuid': find['uuid'],
            'verified': find['verified'],
            'system': find['system'],
        }
    
    if cur is None:
        return sanic.json(body=error_bodys['no_auth'], status=401)
    
    return sanic.json(body=cur) # i don't know how this would be given yet.
