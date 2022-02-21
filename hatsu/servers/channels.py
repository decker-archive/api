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
