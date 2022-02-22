import websockets.exceptions
import logging
from typing import Any
from ..rest import snowflakes
from .opcodes import OpCode

_log = logging.getLogger(__name__)

class ConnectionState:
    def __init__(self, **kwds):
        self.session_id = kwds.get('session_id', snowflakes.snowflake_with_blast(9))
        self.seq: int = kwds.get('seq', 0)

        self.last_seq: int = 0

        self.user_id: int = kwds['user_id']
        self.bot: bool = kwds.get('bot', False)

        self.presence = None
        self.ws = None
        self.compress: bool = kwds.get('compress', False)
        self.large: int = kwds.get('large', 50)

    async def dispatch(self, event_name: str, event_data: Any):
        self.seq += 1
        data = {
            'op': OpCode.DISPATCH,
            't': event_name,
            's': self.seq,
            'd': event_data,
        }

        try:
            if self.ws:
                await self.ws.send(data)
        except websockets.exceptions.ConnectionClosed as exc:
            _log.warning(f'failed to dispatch {event_name!r} to {self.session_id}: {exc!r}')
    
    def usable(self) -> bool:
        return self.ws is not None
