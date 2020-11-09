import requests
import json
import base64
from base64 import b64encode as b


url = "http://localhost:5000/api/v0/message/"

a = {

    "username": "bruh",
    "cookie": "AAAA",
    "time": 1604951915.377928,
    "chatroom": "conv1",
}


res = requests.get(url, json=a)

print(res.text)
#print(base64.b64decode(res.text).decode('utf-8'))
