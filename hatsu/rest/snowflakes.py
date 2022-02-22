import datetime
import time
import hashlib
from snowflake import SnowflakeGenerator

def snowflake_with_blast(instance: int) -> int:
    """Ensures a Snowflakes safe creation, while being original to it's format"""
    time.sleep(0.01)

    return SnowflakeGenerator(instance=instance, epoch=int(1262304001), timestamp=datetime.datetime.now(datetime.timezone.utc).timestamp()).__next__()

def hash_from(snowflake: int = None) -> str:
    """Creates a hash from a snowflake"""
    if snowflake:
        return hashlib.sha1(str(snowflake).encode("utf-8")).hexdigest()
    else:
        return hashlib.sha1(str(snowflake_with_blast(9)).encode("utf-8")).hexdigest()
