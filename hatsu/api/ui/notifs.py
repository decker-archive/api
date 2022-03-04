from ..gateway import send_notification

async def send_friend_notification(requester: int, friender: int, request: bool):
    if request:
        await send_notification('FRIEND_REQUEST', {'requester': requester, 'friender': friender}, requester)
    else:
        await send_notification('FRIEND_REMOVE', {'remover': requester, 'friend': friender}, requester)
