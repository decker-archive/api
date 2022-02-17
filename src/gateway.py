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
import logging
import sanic
from events import events_to_dispatch
from data_bodys import connected_clients, session_ids

async def event_dispatcher(request: sanic.Request, ws):
    while True:
        if request.headers.get('Authorization') in connected_clients:
            for name, data in events_to_dispatch.items():
                logging.debug('< %s', data)
                await ws.send(data)
                events_to_dispatch.pop(name)

async def connect(request: sanic.Request, ws):
    d = ws.recv()
    
    if d['session_id'] in session_ids:
        ...
