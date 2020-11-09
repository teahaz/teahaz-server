import requests
import mimetypes
import json
import base64

def b(a):
    return base64.b64encode(a.encode('utf-8')).decode('utf-8')

while 1:
    url = "http://localhost:5000/api/v0/message/"

    mime = mimetypes.MimeTypes().guess_type('my_file.txt')[0]

    message = input(">> ")

    a = {
        "username": "me",
        "cookie": "test_cookie",
        "chatroom": "conv1",
        "type": "file",
        "mimetype": "",
    }

    res = requests.post(url, json=a)

    print(res.text)
