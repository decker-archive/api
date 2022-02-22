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
}
