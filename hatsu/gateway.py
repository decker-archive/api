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
import quart
from quart import websocket as ws, make_response as r
from .database import users
from .events import events_to_dispatch

app = quart.current_app
clients = set()

async def echo():
    while True:
        d = await ws.receive()
        await ws.send(d)

async def recv():
    queue = asyncio.Queue()
    clients.add(queue)
    while True:
        if ws.authorization == None:
            await ws.close(4001, 'Invalid authorization')
            break
        elif users.find_one({"session_ids": [ws.authorization.password]}) == None:
            await ws.close(4001, 'Invalid authorization')
            break

        for name, data in events_to_dispatch.items():
            d = {
            't': name,
            'd': data
            }
            for client in clients.copy():
                await client
                await ws.send_json(orjson.dumps(d))
            events_to_dispatch.pop(name)
