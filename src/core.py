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
import sanic
import sanic_limiter
from .servers import channels
from .users import create_user, get_me, edit_user
from orjson import dumps
from .gateway import event_send

app = sanic.Sanic('okemia', dumps=dumps)
ratelimiter = sanic_limiter.Limiter(app=app, key_func=sanic_limiter.get_remote_address)

# User Management
app.add_route(create_user, '/v1/users', methods=['POST'])
app.add_route(get_me, '/v1/users/me', methods=['GET'])
app.add_route(edit_user, '/v1/users/edit', methods=['PATCH'])

# Guilds

## Guild Channels
app.add_route(channels.create_channel, '/v1/channels', methods=['POST'])

# Gateway
app.add_websocket_route(event_send, '/v1')

app.run()
