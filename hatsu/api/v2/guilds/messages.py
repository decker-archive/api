from quart import Blueprint, request
from ..database import messages, members
from ..checks import check_session_

msgs = Blueprint('messages', __name__)

@msgs.post('/<int:guild_id>/<int:channel_id>')

@msgs.post('/<int:guild_id>/<int:channel_id>/messages')
async def send_message(channel_id: int):
    creator = await check_session_(request.headers.get('Authorization'))

    member_creator = await members.find_one({'user': {'id': creator['id']}})

