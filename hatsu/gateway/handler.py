import asyncio
import json
from .connection import GatewayConnection
from websockets import server

async def gateway_handler(ws: server.WebSocketServerProtocol):
    try:
        while True:
            r = await ws.recv()

            d: dict = json.loads(r)
    
            connection = GatewayConnection(ws, d.get('encoding', 'json'))
            break

        await connection.run(d)
        await asyncio.Future()
    except asyncio.CancelledError:
        pass
