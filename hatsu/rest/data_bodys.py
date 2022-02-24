import json


error_bodys = {
    'no_auth': json.dumps({
        'code': 401,
        'message': "You aren't supposed to be here! bezerk!"
    }),
    'invalid_data': json.dumps({
        'code': 400,
        'message': 'Invalid data was given'
    }),
    'not_in_guild': json.dumps({
        'code': 401,
        'message': 'You aren\'t in this guild'
    }),
    'missing_perms': json.dumps(
        {
            'code': 401,
            'message': 'You are missing permissions'
        }
    )
}
