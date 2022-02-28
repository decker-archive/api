# utils for using motor, made to make development easier, and faster.
import pymongo
import motor.core as motor
import motor.motor_asyncio as motor_
import dotenv
import os

dotenv.load_dotenv()

client: motor.AgnosticClient = motor_.AsyncIOMotorClient(os.getenv('mongo_uri'))

# databases.
_users: motor.AgnosticDatabase = client.get_database('users', read_preference=pymongo.ReadPreference.SECONDARY)
_guilds: motor.AgnosticDatabase = client.get_database(
    'guilds', read_preference=pymongo.ReadPreference.SECONDARY
)
_dms: motor.AgnosticDatabase = client.get_database(
    'direct_messages', read_preference=pymongo.ReadPreference.SECONDARY
)
_events: motor.AgnosticDatabase = client.get_database('events')

# users, core
users: motor.AgnosticCollection = _users.get_collection('core', read_preference=pymongo.ReadPreference.SECONDARY)

# guilds
members: motor.AgnosticCollection = _guilds.get_collection(
    'members', read_preference=pymongo.ReadPreference.SECONDARY
)
channels: motor.AgnosticCollection = _guilds.get_collection(
    'channels', read_preference=pymongo.ReadPreference.SECONDARY
)
messages: motor.AgnosticCollection = _guilds.get_collection(
    'messages', read_preference=pymongo.ReadPreference.SECONDARY
)

# dms
normal_dm: motor.AgnosticCollection = _dms.get_collection(
    'normal', read_preference=pymongo.ReadPreference.SECONDARY
)
group_dm: motor.AgnosticCollection = _dms.get_collection(
    'groups', read_preference=pymongo.ReadPreference.SECONDARY
)

# the guilds the user is in (partial  object.)
guilds: motor.AgnosticCollection = _guilds.get_collection('core')

joined_guilds: motor.AgnosticCollection = _users.get_collection('guilds')

# core events
events: motor.AgnosticCollection = _events.get_collection('core')

guild_invites: motor.AgnosticCollection = _guilds.get_collection('invites')
