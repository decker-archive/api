# utils for using motor, made to make development easier, and faster.
import asyncio
import pymongo
import motor.core as motor
import motor.motor_asyncio as motor_
import dotenv
import os

dotenv.load_dotenv()


loop = asyncio.new_event_loop()
client: motor.AgnosticClient = motor_.AsyncIOMotorClient(
    os.getenv('mongo_uri'), io_loop=loop
)

# databases.
_users: motor.AgnosticDatabase = client.get_database(
    'users', read_preference=pymongo.ReadPreference.SECONDARY
)
_guilds: motor.AgnosticDatabase = client.get_database(
    'guilds', read_preference=pymongo.ReadPreference.SECONDARY
)
_dms: motor.AgnosticDatabase = client.get_database(
    'direct_messages', read_preference=pymongo.ReadPreference.SECONDARY
)

# users, core
users: motor.AgnosticCollection = _users.get_collection(
    'core', read_preference=pymongo.ReadPreference.SECONDARY
)

# guilds
channels: motor.AgnosticCollection = _guilds.get_collection(
    'channels', read_preference=pymongo.ReadPreference.SECONDARY
)

messages: motor.AgnosticCollection = _guilds.get_collection('messages')

members: motor.AgnosticCollection = _guilds.get_collection('members')

# dms
normal_dm: motor.AgnosticCollection = _dms.get_collection(
    'normal', read_preference=pymongo.ReadPreference.SECONDARY
)
group_dm: motor.AgnosticCollection = _dms.get_collection(
    'groups', read_preference=pymongo.ReadPreference.SECONDARY
)

guilds: motor.AgnosticCollection = _guilds.get_collection('core')

guild_invites: motor.AgnosticCollection = _guilds.get_collection('invites')

user_interface: motor.AgnosticCollection = _users.get_collection('ui')

user_agent_tracking: motor.AgnosticCollection = _users.get_collection('user-agents')

user_settings: motor.AgnosticCollection = _users.get_collection('settings')

friends: motor.AgnosticCollection = _users.get_collection('friends')

async def _init_indexes():
    # guild-specific

    messages.create_index('content')
    messages.create_index('created_at')

    members.create_index('joined_at')
    members.create_index('owner')
    members.create_index('roles')

    guild_invites.create_index('guild_id')

    guilds.create_index('name')
    guilds.create_index('created_at')
    guilds.create_index('owner')

    # users

    users.create_index('username')
    users.create_index('separator')

    friends.create_index('other')

    # direct messages

    normal_dm.create_index('users')

    group_dm.create_index('users')
