import fastapi
import datetime

app = fastapi.FastAPI(title="Stancium API", version="v1", description="The RESTFul and Gateway Stancium API")

errors = {
    "Bye": {
        'message': 'You are not authorized to be here, bezerk!',
        'status': 401
    }
}

# should be replaced with a database.
users = {
    '': {
        'username': 'VincentRPS',
        'email': 'yourmomxox@hotmail.com',
        'password': 'password',
    }
}
def now(): return datetime.datetime.now(datetime.timezone.utc)

def flaker(): return int(now.timestamp() * 1000 - 1262307601) << 22 | 0x3FFFFF

# this doesn't really work.
@app.post("/signup")
async def signup(inter: fastapi.Response, req: fastapi.Request):
    r = await req.json()
    inter.status_code = 200
    return r, inter
