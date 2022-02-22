import logging
import urllib.parse
from quart import Quart
from .core import WebSocket
from ..rest.database import users
from websockets.server import WebSocketServerProtocol


async def gateway_handler(app: Quart, ws: WebSocketServerProtocol, url: str):
    args = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    logging.debug(f'{ws.id} has connected to the gateway')

    if users.find_one({'session_ids': [ws.extra_headers.get('Session-ID', '')]}) == None:
        return await ws.close(4001, 'Invalid Headers')
    
    try:
        version = args['v'][0]
    except(IndexError, KeyError):
        version = 1
    
    try:
        encoding = args['encoding'][0]
    except(KeyError, IndexError):
        encoding = 'json'
    
    if version not in (1):
        return await ws.close(4000, 'Invalid Gateway Version')
    
    if encoding not in ('json', 'etf'):
        return await ws.close(4000, 'Invalid Encoding Type')
    
    try:
        compress = args['compress'][0]
    except(KeyError, IndexError):
        compress = None

    async with app.app_context():
        gateway = WebSocket(
            ws,
            version=int(version),
            encoding=encoding,
            compress=compress
        )

        await gateway.run()
