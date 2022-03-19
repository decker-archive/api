import ulid
import hashlib
from .database import guild_invites

Snowflake = str

def hash_from(snowflake: Snowflake = None) -> str:
    if snowflake:
        return hashlib.sha1(str(snowflake).encode("utf-8")).hexdigest()
    else:
        return hashlib.sha1(str(ulid.new().str)).encode("utf-8").hexdigest()


async def gen_code() -> str:
    import secrets
    import re

    raw = secrets.token_urlsafe(10)
    raw = re.sub(r"\/|\+|\-|\_", "", raw)

async def invite_code() -> str:
    raw = await gen_code()

    check = await guild_invites.find_one({'code': raw})

    if check != None:
        return await invite_code()

    return raw[:7]
