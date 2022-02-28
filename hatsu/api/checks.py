from .database import users, members


async def check_session_(session_id):
    user = await users.find_one({'session_ids': [session_id]})

    if user == None:
        return None
    else:
        return user


async def check_if_in_guild(ver):
    member = await members.find_one({'id': ver['id']})

    if member == None:
        return None
    else:
        return member
