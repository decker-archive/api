import requests


r = requests.get("http://127.0.0.1:8000/v1/users/@me", headers={"Authorization": ""})

print(r.json())