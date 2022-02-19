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

# databases.
_users = client.get_database('users', read_preference=pymongo.ReadPreference.SECONDARY)
_servers = client.get_database('servers', read_preference=pymongo.ReadPreference.SECONDARY)
_dms = client.get_database('direct_messages', read_preference=pymongo.ReadPreference.SECONDARY)

# users, core
users = _users.get_collection('core', read_preference=pymongo.ReadPreference.SECONDARY)

# servers
members = _servers.get_collection('members', read_preference=pymongo.ReadPreference.SECONDARY)
channels = _servers.get_collection('channels', read_preference=pymongo.ReadPreference.SECONDARY)
messages = _servers.get_collection('messages', read_preference=pymongo.ReadPreference.SECONDARY)
roles = _servers.get_collection('roles', read_preference=pymongo.ReadPreference.SECONDARY)

# dms
normal_dm = _dms.get_collection('normal', read_preference=pymongo.ReadPreference.SECONDARY)
group_dm = _dms.get_collection('groups', read_preference=pymongo.ReadPreference.SECONDARY)

# the servers the user is in (partial server object.)
servers = _users.get_collection('servers')

# while this is probably cutting some corners 
# and could make gateway connections slightly more slower,
# it is the only thing i could think of for this.
gateway = client.get_database('gateway')
