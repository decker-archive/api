import datetime
import hashlib
import uuid
import time
from snowflake import SnowflakeGenerator

seq = 0
instance = 0

def snowflake_with_blast() -> int:
    """Ensures a Snowflakes safe creation, while being original to it's format"""
    global instance
    global seq

    if seq == 4095:
        seq = 0
    
    if instance == 1023:
        instance = 0
    
    seq += 1
    instance += 1

    return SnowflakeGenerator(
        instance=instance,
        epoch=int(1262304001),
        seq=int(seq),
        timestamp=datetime.datetime.now(datetime.timezone.utc).timestamp(),
    ).__next__()


def hash_from(snowflake: int = None) -> str:
    """Creates a hash from a snowflake"""
    if snowflake:
        return hashlib.sha1(str(snowflake).encode("utf-8")).hexdigest()
    else:
        return hashlib.sha1(str(snowflake_with_blast()).encode("utf-8")).hexdigest()

def invite_code() -> str:
    return uuid.uuid4().hex[-7:]
