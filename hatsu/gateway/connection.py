import asyncio
import zlib
import json
from ..rest.database import users
from typing import Sequence, Any, Set, Union, List
from websockets import server, exceptions

def yield_chunks(input_list: Sequence[Any], chunk_size: int):
    for idx in range(0, len(input_list), chunk_size):
        yield input_list[idx : idx + chunk_size]

def byte(data: Union[str, bytes]) -> bytes:
    return data if isinstance(data, bytes) else data.encode()

class GatewayConnection:
    def __init__(self, ws: server.WebSocketServerProtocol, encoding: str):
        self.ws = ws
        self.closed: bool = False
        self.encoding = encoding

        # intitiate zlib things
        self.deflator = zlib.compressobj()
    
    async def check_session_id(self):
        while True:
            if self.closed:
                break
            
            if users.find_one({'session_ids': [self.session_id]}) == None:
                await self.ws.close(4002, 'Invalid authorization')
                break
            else:
                find = users.find_one({'session_ids': [self.session_id]})
                to_give = {
                    'id': find['id'],
                    'username': find['username'],
                    'separator': find['separator'],
                    'avatar_url': find['avatar_url'],
                    'banner_url': find['banner_url'],
                    'flags': find['flags'],
                    'verified': find['verified'],
                    'system': find['system'],
                }
                self.user_info = json.dumps(to_give)
                break
    
    async def __send(self, data: bytes, chunk_size: int):
        await self.ws.send(yield_chunks(data, chunk_size))
    
    async def _send(self, data):
        d1 = self.deflator.compress(data)
        d2 = self.deflator.flush(zlib.Z_FULL_FLUSH)
        d = d1 + d2

        await self.__send(d, 1024)
    
    async def send(self, payload: Any):
        if isinstance(payload, dict):
            if self.encoding == 'json':
                await self.ws.send(json.dumps(payload))
            else:
                await self._send(byte(json.dumps(payload)))
        else:
            await self._send(byte(payload))
    
    async def do_hello(self):
        await self.send({
            't': 'HELLO',
            's': self.session_id,
            'd': None,
            'i': 'Sent once we have verified your session_id, '
            'the data given will be null. '
            'please wait for the READY event before continuing-'
            '-with any requests.'
        })
    
    async def do_ready(self):
        await self.send({
            't': 'READY',
            's': self.session_id,
            'd': self.user_info,
            'i': None,
        })

    async def poll_recv(self, data: dict):
        if data.get('t', '') == 'HEARTBEAT':
            await self.send({
                't': 'ACK',
                '_s': self.session_id,
                's': data.get('s', ''),
                'd': None,
            })
        
    async def do_recv(self):
        while True:
            if self.closed:
                connections.remove(self)
                del self
                break

            try:
                r = await self.ws.recv()
                await self.poll_recv(json.loads(r))
            except exceptions.ConnectionClosedOK:
                self.closed = True
                break

    async def run(self, data: dict):
        if self.encoding not in ('json', 'zlib'):
            await self.ws.close(4004, 'Invalid encoding')
            self.closed = True
            return
        connections.add(self.ws)
        self.session_id = data.get('session_id', '')
        await self.check_session_id()

        await self.do_hello()
        await asyncio.sleep(9)
        await self.do_ready()
        try:
            await self.do_recv()
        except exceptions.ConnectionClosedError:
            return

connections: Set[server.WebSocketServerProtocol] = set()

async def dispatch_event(event_name: str, data: dict):
    d = {
        't': event_name.upper(),
        'd': data
    }
    for connection in connections.copy():
        await connection.send(json.dumps(d))
