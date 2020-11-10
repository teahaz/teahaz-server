import requests
import mimetypes
import json
import base64

def b(a):
    return base64.b64encode(a.encode('utf-8')).decode('utf-8')

while 1:
    url = "http://localhost:5000/api/v0/file/"

    #mime = mimetypes.MimeTypes().guess_type('my_file.txt')[0]

    filename = input(">> ")

    a = {
        "username": "me",
        "cookie": "test_cookie",
        "chatroom": "conv1",
        "type": "file",
    }

    # streaming uploads like this make it so the file is never fully loaded into memory
    # im sorry but this one thing will change a lot, but ill probably make a function that is a drop in replacement and you wont have to bother with it
    with open(filename, 'rb') as f:
        res = requests.post(url, json=a, data=f)


    print(res.text)
