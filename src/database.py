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
# utils for using motor, made to make development easier, and faster.
import pymongo
import dotenv
import os

dotenv.load_dotenv()

client = pymongo.MongoClient(os.getenv('mongo_uri'))

_users = client.get_database('users', read_preference=pymongo.ReadPreference.SECONDARY)

users = _users.get_collection('core', read_preference=pymongo.ReadPreference.SECONDARY)
