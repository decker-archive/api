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

_messages: motor.AgnosticDatabase = client.get_database(
    'messages', read_preference=pymongo.ReadPreference.PRIMARY
)

# users, core
users: motor.AgnosticCollection = _users.get_collection(
    'core', read_preference=pymongo.ReadPreference.SECONDARY
)

# guilds
channels: motor.AgnosticCollection = _guilds.get_collection(
    'channels', read_preference=pymongo.ReadPreference.SECONDARY
)

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

async def send_message(channel_id: str, data: dict):
    col: motor.AgnosticCollection = _messages.get_collection(channel_id)
    await col.create_index('content')
    await col.create_index('created_at')
    await col.create_index('channel_id')

    data['channel_id'] = channel_id

    await col.insert_one(data)

async def get_message(channel_id: str, message_id: str):
    c: motor.AgnosticCursor = await channels.find({'_id': channel_id})

    cc = await c.to_list(1)

    if cc == []:
        return None

    col: motor.AgnosticCollection = _messages.get_collection(channel_id)
    
    return await col.find_one({'channel_id': channel_id, '_id': message_id})

async def edit_message(channel_id: str, message_id: str, data: dict):
    col: motor.AgnosticCollection = _messages.get_collection(channel_id)

    await col.update_one({'_id': message_id}, data)

async def delete_message(channel_id: str, message_id: str):
    col: motor.AgnosticCollection = _messages.get_collection(channel_id)

    await col.delete_one({'_id': message_id})

async def _init_indexes():
    # guild-specific

    await members.create_index('joined_at')
    await members.create_index('owner')
    await members.create_index('roles')

    await guild_invites.create_index('guild_id')
    await guild_invites.create_index('code')

    await guilds.create_index('name')
    await guilds.create_index('created_at')
    await guilds.create_index('owner')

    # users

    await users.create_index('username')
    await users.create_index('separator')

    await friends.create_index('other')

    # direct messages

    await normal_dm.create_index('users')

    await group_dm.create_index('users')
