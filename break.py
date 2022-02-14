import datetime
import time
from snowflake import SnowflakeGenerator

def snowflake_with_blast(instance: int) -> int:
    time.sleep(0.01)
    return SnowflakeGenerator(instance=instance, epoch=int(1262304001), timestamp=datetime.datetime.now(datetime.timezone.utc).timestamp()).__next__()

while True:
    # the epoch in this case is the first second of 2010

    print(snowflake_with_blast(1))
    print(snowflake_with_blast(2))
    print(snowflake_with_blast(3))
    print(snowflake_with_blast(4))
