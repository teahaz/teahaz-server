import requests
import json
import base64

def b(a):
    return base64.b64encode(a.encode('utf-8')).decode('utf-8')

while 1:
    url = "http://localhost:5000/api/v0/message/"

    message = input(">> ")
    print(type(b(message)))

    a = {
        "username": "me",
        "cookie": "test_cookie",
        "type": "text",
        "chatroom": "conv1",
        "message": b(message)
    }

    res = requests.post(url, json=a)

    print(res.text)
