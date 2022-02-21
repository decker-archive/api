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
from typing import Any
from collections import OrderedDict
from .snowflakes import snowflake_with_blast

async def add_event(event, data):
    events_to_dispatch[snowflake_with_blast(9)] = data

events_to_dispatch: OrderedDict[str, OrderedDict[str, Any]] = OrderedDict()
