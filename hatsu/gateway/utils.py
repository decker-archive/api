import asyncio
import logging
from typing import Any, Coroutine, Sequence, Union


def yield_chunks(input: Sequence[Any], chunk_size: int):
    for i in range(0, len(input), chunk_size):
        yield input[i:i+chunk_size]

def want_bytes(data: Union[str, bytes]) -> bytes:
    return data if isinstance(data, bytes) else data.encode()


def want_string(data: Union[str, bytes]) -> str:
    return data.decode() if isinstance(data, bytes) else data

async def task_wrap(name: str, coro: Coroutine):
    try:
        await coro
    except asyncio.CancelledError:
        pass
    except Exception as exc:
        logging.error(f'Error happend with task {name}: {exc}')
