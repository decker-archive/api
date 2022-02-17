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
from .users import create_user, get_me, edit_user
from .gateway import event_dispatcher, connect
from orjson import dumps

app = sanic.Sanic('okemia', dumps=dumps)

app.add_route(create_user, '/users/create', methods=['POST'])
app.add_route(get_me, '/users/me', methods=['GET'])
app.add_route(edit_user, '/users/edit', methods=['PATCH'])
app.add_websocket_route(event_dispatcher, '/gateway/events')
app.add_websocket_route(connect, '/gateway')

app.run()