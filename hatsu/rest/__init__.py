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
import os
import dotenv
import quart_rate_limiter
from quart import Quart
from .servers import channels
from .users import create_user, get_me, edit_user

app = Quart(__name__)
dotenv.load_dotenv()

rates = quart_rate_limiter.RateLimiter(app=app)

# users
app.add_url_rule('/v1/users/@me', view_func=create_user, methods=['POST'])
app.add_url_rule('/v1/users/@me', view_func=get_me, methods=['GET'])
app.add_url_rule('/v1/users/@me', view_func=edit_user, methods=['PATCH'])

app.run(host='0.0.0.0')
