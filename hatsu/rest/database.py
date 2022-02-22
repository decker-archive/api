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
_events = client.get_database('events')

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

# core events
events = _events.get_collection('core')
