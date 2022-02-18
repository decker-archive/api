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
import orjson
import sanic
from ..database import channels, users
from ..data_bodys import error_bodys
from ..ratelimiting import ratelimiter

@ratelimiter.limit('20/minute')
async def create_channel(request: sanic.Request):
    auth = request.headers.get('Authorization')
    ver = users.find_one({'session_ids': [auth]})
    let = False

    for session_id in ver['session_ids']:
        if session_id == auth:
            let = True
    
    if let == False:
        return sanic.json(error_bodys['no_auth'], 401)
    d: dict = request.load_json(loads=orjson.loads)
    try:
        data = {
            'name': d['name'],

        }
    except KeyError:
        return sanic.json(error_bodys['invalid_data'])
