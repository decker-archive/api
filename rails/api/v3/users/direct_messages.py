from quart import request, Response, Blueprint
from ..database import normal_dm, group_dm, friends

group_dms = Blueprint('group-dms-v3', __name__)

@group_dms('/direct-messages/groups/create')
async def create_group_dm():
    ...
