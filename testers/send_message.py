import requests
import json
from base64 import b64encode as b

while 1:
    url = "http://localhost:5000/api/v0/send/"
    
    message = input(">> ")

    a = {
            'username':b(b'fuckface').decode('utf-8'),
            'cookie': b(b'AAAAA').decode('utf-8'),
            'type': b(b'text').decode('utf-8'),
            'message': b(message.encode("utf-8")).decode('utf-8')
    }

    res = requests.post(url, json=a)

    print(res.text)
