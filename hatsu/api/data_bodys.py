import json

error_bodys = {
    'no_auth': json.dumps({'code': 0, 'message': "401: Unauthorized"}),
    'invalid_data': json.dumps({'code': 0, 'message': '400: Bad Request'}),
    'not_in_guild': json.dumps({'code': 0, 'message': '403: Unauthorized'}),
    'missing_perms': json.dumps({'code': 0, 'message': '401: Unauthorized'}),
    'not_found': json.dumps({'code': 0, 'message': '404: Not Found'}),
    'already_in_guild': json.dumps({'code': 0, 'message': '409: You are already in this guild'})
}
