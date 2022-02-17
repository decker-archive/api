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
from .data_bodys import error_bodys

async def create_user(require: sanic.Request):
    d = require.load_json(loads=orjson.loads)

async def get_me(require: sanic.Request):
    auth = require.headers.get('Authorization')

    ret = None
    
    if ret is None:
        return sanic.json(body=error_bodys['no_auth'], status=401)
    
    return sanic.json(body=ret)
