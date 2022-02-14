import sanic
from orjson import dumps

app = sanic.Sanic('oshinor', dumps=dumps)

auths = {
    'bruh': {
        'username': 'VincentRPS',
        'auth': 'bruh'
    }
}

bodys = {
    'no_auth': "You aren't supposed to be here! bezerk!"
}

@app.get('/users/me')
async def get_me(require: sanic.Request):
    auth = require.headers.get('Authorization')
    ret = None
    for user in auths.values():
        if user['auth'] == auth:
            ret = user
    
    if ret is None:
        return sanic.json(body=bodys['no_auth'], status=401)
    
    return sanic.json(body=ret)

app.run()