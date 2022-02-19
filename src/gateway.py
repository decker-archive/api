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
import asyncio
import orjson
import sanic
from sanic.server.websockets import impl
from .database import users
from .events import events_to_dispatch
from .snowflakes import hash_from

async def event_send(req: sanic.Request, ws: impl.WebsocketImplProtocol):
    while True:
        events_already_given = {}
        if req.headers.get('Authorization') == None:
            await ws.close(4001, 'No authorization provided')
            break
            
        a = req.headers.get('Authorization')
        if users.find_one({'session_ids': [a]}) == None:
            await ws.close(4001, 'No authorization provided')
            break


        for name, data in events_to_dispatch.items():
            s = {
                's': name,
                'd': data
            }

            if data in events_already_given.values():
                pass
            else:
                events_already_given[hash_from()] = s
                await ws.send(orjson.dumps(s))
        
        await asyncio.sleep(1)

        events_already_given.clear()
