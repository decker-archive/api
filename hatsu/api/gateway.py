import json
from websockets import client
from asyncio import get_running_loop, sleep


async def connect():
    global ws
    ws = await client.connect(
        'wss://gateway.vincentrps.xyz/', ping_timeout=30, close_timeout=1000000000
    )
    await ws.send(
        json.dumps({'session_id': 'adb8ddecad0ec633da6651a1b441026fdc646892'})
    )
    await check_if_closed()


async def check_if_closed():
    await sleep(1)
    global ws
    if ws.closed:
        try:
            ws = await client.connect('wss://gateway.vincentrps.xyz', ping_timeout=30)
            await ws.send(
                json.dumps({'session_id': 'adb8ddecad0ec633da6651a1b441026fdc646892'})
            )
        except:
            get_running_loop().create_task(check_if_closed())
    else:
        await sleep(5)
        get_running_loop().create_task(check_if_closed())


async def dispatch_event(event_name: str, event_data: dict):
    d = {'t': 'DISPATCH', 'd': {'name': event_name.upper(), 'data': event_data}}
    await ws.send(json.dumps(d))


async def dispatch_event_to(user_id: int, event_name: str, event_data: dict):
    d = {
        't': 'DISPATCH_TO',
        'd': {'event_name': event_name.upper(), 'data': event_data, 'user': user_id},
    }
    await ws.send(json.dumps(d))


async def guild_dispatch(guild_id: int, event_name: str, event_data: dict):
    d = {
        't': 'DISPATCH_TO_GUILD',
        'd': {'guild_id': guild_id, 'event_name': event_name, 'data': event_data},
    }
    await ws.send(json.dumps(d))


async def send_notification(type: str, excerpt: dict):
    d = {'t': 'NOTIFICATION', 'type': str(type), 'excerpt': excerpt}
    await ws.send(json.dumps(d))
