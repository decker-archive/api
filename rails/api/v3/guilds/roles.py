from quart import Blueprint
from ..database import r

rolesbp = Blueprint('roles-v3', __name__)

@rolesbp.post('/roles/create')
async def create_role():
    ...

@rolesbp.post('/<guild_id>/<member_id>/roles')
async def give_role(guild_id, member_id):
    ...
