import requests

r = requests.get("http://localhost:8000/users/me", headers={'Authorization': 'bruh'})

print(r.text)