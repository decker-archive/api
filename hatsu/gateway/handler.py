import urllib.parse
from quart import Quart
from .core import WebSocket


async def gateway_handler(app: Quart, ws, url: str):
    args = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)

    
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
