import asyncio
import logging
import zlib
import random
import websockets.exceptions
import zstandard as zstd
from typing import Any, Dict
from collections import namedtuple
from quart import current_app
from .encoding import (
    compress_json, 
    decompress_json, 
    compress_earl, 
    decompress_earl
)
from .utils import (
    want_bytes, 
    want_string, 
    yield_chunks,
    task_wrap
)
from .opcodes import OpCode

Properties = namedtuple(
    'Properties', 'version encoding compress zctx zsctx tasks'
)

_log = logging.getLogger(__name__)
null = None

class WebSocket:
    def __init__(self, ws, *, version: int, encoding, compress):
        self.app = current_app
        self.ws = ws
        self.version = version
        self.encoding = encoding
        self.compress = compress
        self.properties = Properties(
            version,
            encoding,
            compress,
            zlib.decompressobj(),
            zstd.ZstdCompressor(),
            {}
        )
        self.loop = asyncio.get_running_loop()

        self.heartbeat_counter = 0
        self.trace = f'hatsu-prod-{random.randint(1, 10)}'
        self.closed: bool = False
    
    def _set_encoding(self):
        encoding = self.properties.encoding

        encodings = {
            'json': (compress_json, decompress_json),
            'etf': (compress_earl, decompress_earl),
        }

        self.encoder, self.decoder = encodings[encoding]
    
    async def _zlib_stream_send(self, encoded_data):
        first_data = self.properties.zctx.compress(encoded_data)
        second_data = self.properties.zctx.flush(zlib.Z_FULL_FLUSH)
        data = first_data + second_data

        _log.debug('zlib-stream: length %s -> compressed (%s)', len(encoded_data), len(data))

        await self.send_chunks(data, 1024)
    
    async def send_chunks(self, data: bytes, chunk_size: int):
        _log.debug('zlib-stream: sending {b} bytes into {e}-byte chunks'.format(b=len(data), e=chunk_size))

        await self.ws.send(yield_chunks(data, chunk_size))
    
    async def send(self, data: Dict[str, Any]):
        encoded = self.encoder(data)

        _log.debug(f'< op: {data.get("op")}, s: {data.get("s")}, t: {data.get("t")}')

        if isinstance(encoded, str):
            encoded = encoded.encode()
        
        if self.properties.compress == 'zlib-stream':
            await self._zlib_stream_send(want_bytes(encoded))
        elif (
            self.state
            and self.state.compress
            and len(encoded) > 8192
            and self.properties.compress != 'etf'
        ):
            await self.ws.send(zlib.compress(want_bytes(encoded)))
        else:
            await self.ws.send(want_bytes(encoded) if self.properties.encoding == 'etf' else want_string(encoded))
    
    def heartbeat_start(self, interval: int):
        task = self.properties.tasks.get('heartbeat')
        if task:
            task.cancel()
        
        self.properties.tasks['heartbeat'] = self.loop.create_task(
            task_wrap('hb wait', self.heartbeat_wait(interval))
        )
    
    async def heartbeat_wait(self, interval: int):
        await asyncio.sleep(interval / 1000)
        await self.ws.close(4000, 'Session timed out')
        self.closed = True
    
    async def ready(self):

        _data = {
            'op': OpCode.READY,
            't': null,
            'd': {
                'v': self.properties.version,
                '_trace': [self.trace],
                'session_id': self.state.session_id,
                'shard': 0, 
            }
        }

        data = _data

        await self.send(data)
    
    async def handle_opcode_1(self, payload):
        self.heartbeat_counter += 1
    
    def cleanup(self):
        for task in self.properties.tasks.values():
            task.cancel()
        
        if self.state:
            self.state.ws = None
            self.state = None
        
        self.closed = True
    
    async def send_hello(self):
        interval = random.randint(40, 46) * 1000

        await self.send({
        'op': OpCode.HELLO,
        't': null,
        's': null,
        'd': {
            'heartbeat_interval': interval,
            '_trace': [self.trace]
        }
    })

    async def listen_for_messages(self):
        while True:
            if self.closed:
                break
            msg = await self.ws.recv()
            if len(msg) > 4068:
                await self.ws.close(4001, 'Payload length exceeded')
            payload = self.encoder(msg)
            _log.debug(f'Received\n{payload}')
    
    async def process_message(self, payload):
        try:
            op = payload['op']
        except KeyError:
            await self.ws.close(4002, 'No OpCode Given')
            return
        
        try:
            handler = getattr(self, f'handle_opcode_{op}')
        except AttributeError:
            await self.ws.close(4003, 'Invalid OpCode given')
            return
        
        await handler(payload)    
    
    async def run(self):
        try:
            async with self.app.app_context():
                await self.send_hello()
                await self.listen_for_messages()
        except websockets.exceptions.ConnectionClosed as exc:
            _log.error(exc)
        except Exception as exc:
            _log.error(exc)
        finally:
            self.cleanup()
