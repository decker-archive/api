import json
import re

error_bodys = {
    'no_auth': json.dumps({'code': 0, 'message': "401: Unauthorized"}),
    'invalid_data': json.dumps({'code': 0, 'message': '400: Bad Request'}),
    'not_in_guild': json.dumps({'code': 0, 'message': '403: Unauthorized'}),
    'missing_perms': json.dumps({'code': 0, 'message': '401: Unauthorized'}),
    'not_found': json.dumps({'code': 0, 'message': '404: Not Found'}),
    'already_in_guild': json.dumps(
        {'code': 0, 'message': '409: You are already in this guild'}
    ),
    'no_perms': json.dumps({'code': 0, 'message': '403: Forbidden'}),
    'no_content': json.dumps({'code': 0, 'message': '204: No Content'}),
}

mention = re.compile('<@!*&*[0-9]+>')
emote = re.compile('<:\w+:[0-9]+>')
channels = re.compile('<#[0-9]+>')