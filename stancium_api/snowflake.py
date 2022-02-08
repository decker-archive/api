#!/usr/bin/env python
import datetime

# the stancium epoch is simply the first day of 2022.
# 1640998801
def create_snowflake() -> int:
    dt = datetime.datetime.now(datetime.timezone.utc)
    snowflake = int(dt.timestamp() * 1000 - 1640998801) << 22 | 0x3fffff
    return snowflake
