import requests
import json
import base64
from base64 import b64encode as b


url = "http://localhost:5000/api/get/"

a = {
        'username': b(b'fuckface').decode('utf-8'),
        'cookie': b(b'AAAAA').decode('utf-8'), 
        'last_get_time':b(b"1597017007.553126").decode("utf-8")
}


res = requests.post(url, json=a)

print(base64.b64decode(res.text).decode('utf-8'))
