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
from typing import Set
import orjson
import asyncio
import sanic
from sanic.server.websockets import impl
from .database import users
from .events import events_to_dispatch

clients: Set[impl.WebsocketImplProtocol] = set()
sending_events: bool = False

async def send_events():
    for ws in clients:
        for name, data in events_to_dispatch.items():
            s = {
                's': name,
                'd': data
            }
            await ws.send(orjson.dumps(s))
    
    await asyncio.sleep(0.3)
    
    await send_events()

async def event_send(req: sanic.Request, ws: impl.WebsocketImplProtocol):
    while True:
        if req.headers.get('Authorization') == None:
            await ws.close(4001, 'No authorization provided')
            break
            
        a = req.headers.get('Authorization')

        if users.find_one({'session_ids': [a]}) == None:
            await ws.close(4001, 'No authorization provided')
            break
            
        clients.add(ws)

        if not sending_events:
            send_events = True
            await send_events()
