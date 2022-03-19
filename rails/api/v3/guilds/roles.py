from quart import Blueprint
from ..database import r

rolesbp = Blueprint('roles-v3', __name__)

@rolesbp.post('')
async def create_role():
    ...
