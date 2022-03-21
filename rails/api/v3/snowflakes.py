import snowflake as _snowflake
import hashlib
import dotenv
import uuid
import os
import time

dotenv.load_dotenv()
generator = _snowflake.Generator(1448841601000, int(os.getenv('process_id', 0)), int(os.getenv('worker_id', 0)))

def snowflake():
    return str(generator.generate(int(round(time.time() * 1000))))

def hash_from(snowflake_: str = None) -> str:
    if snowflake_:
        return hashlib.sha384(str(snowflake_).encode("utf-8")).hexdigest()
    else:
        return hashlib.sha384(snowflake().encode("utf-8")).hexdigest()

def code():
    return uuid.uuid1()
