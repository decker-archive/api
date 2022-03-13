import json
import re

error_bodys = {
    'no_auth': json.dumps({'message': "401: Unauthorized", 'code': 0, }),
    'invalid_data': json.dumps({'message': '400: Bad Request', 'code': 0, }),
    'not_in_guild': json.dumps({'message': '403: Unauthorized', 'code': 0, }),
    'missing_perms': json.dumps({'message': '401: Unauthorized', 'code': 0, }),
    'not_found': json.dumps({'message': '404: Not Found', 'code': 0,}),
    'already_in_guild': json.dumps(
        {'message': '409: You are already in this guild', 'code': 0, }
    ),
    'no_perms': json.dumps({'message': '403: Forbidden', 'code': 0,}),
    'no_content': json.dumps({'message': '204: No Content', 'code': 0,}),
}

mention = re.compile('<@!*&*[0-9]+>')
emote = re.compile('<:\w+:[0-9]+>')
channels = re.compile('<#[0-9]+>')
