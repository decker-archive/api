from .database import events

async def add_event(event, data):
    events.insert_one({'t': event, 'd': data})

