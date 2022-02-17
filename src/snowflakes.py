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
import datetime
import time
from snowflake import SnowflakeGenerator

def snowflake_with_blast(instance: int) -> int:
    """Ensures a Snowflakes safe creation, while being original to it's format"""
    time.sleep(0.01)
    return SnowflakeGenerator(instance=instance, epoch=int(1262304001), timestamp=datetime.datetime.now(datetime.timezone.utc).timestamp()).__next__()
