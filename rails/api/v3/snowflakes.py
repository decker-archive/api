import datetime
import hashlib
from .database import guild_invites
from ..couped.snowflake import snowflake

seq = 0
instance = 0


def snowflake_with_blast():
    """Ensures a Snowflakes safe creation, while being original to it's format"""
    return str(snowflake())

def hash_from(snowflake: int = None) -> str:
    """Creates a hash from a snowflake"""
    if snowflake:
        return hashlib.sha1(str(snowflake).encode("utf-8")).hexdigest()
    else:
        return hashlib.sha1(str(snowflake_with_blast()).encode("utf-8")).hexdigest()


async def invite_code() -> str:
    import secrets
    import re

    raw = secrets.token_urlsafe(10)
    raw = re.sub(r"\/|\+|\-|\_", "", raw)

    check = await guild_invites.find_one({'code': raw})

    if check != None:
        return await invite_code()

    return raw[:7]
