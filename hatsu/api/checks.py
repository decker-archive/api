import quart
from .database import users, members
from .data_bodys import error_bodys


def check_session_(session_id):
    user = users.find_one({'session_ids': [session_id]})

    if user == None:
        return None
    else:
        return user


def check_if_in_guild(ver):
    member = members.find_one({'id': ver['id']})

    if member == None:
        return None
    else:
        return member
