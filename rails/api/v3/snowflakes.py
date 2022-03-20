import snowflake as _snowflake
import hashlib
import dotenv
import os
from .database import guild_invites

dotenv.load_dotenv()
Snowflake = str
generator = _snowflake.Generator(1647723327, int(os.getenv('process_id', 0)), int(os.getenv('worker_id', 0)))

def snowflake():
    return str(generator.generate())

def hash_from(snowflake_: Snowflake = None) -> str:
    if snowflake_:
        return hashlib.sha1(str(snowflake_).encode("utf-8")).hexdigest()
    else:
        return hashlib.sha1(snowflake()).encode("utf-8").hexdigest()


def gen_code() -> str:
    import secrets
    import re

    raw = secrets.token_urlsafe(10)
    raw = re.sub(r"\/|\+|\-|\_", "", raw)

async def invite_code() -> str:
    raw = gen_code()

    check = await guild_invites.find_one({'code': raw})

    if check != None:
        return await invite_code()

    return raw[:7]
