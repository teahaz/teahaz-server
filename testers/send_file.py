import requests
import mimetypes
import json
import base64

def b(a):
    return base64.b64encode(a.encode('utf-8')).decode('utf-8')

while 1:
    url = "http://localhost:5000/api/v0/file/"

    filename = input(">> ")
    if len(filename) == 0:
        filename = '../notes.md'
    print(filename)

    mime = mimetypes.MimeTypes().guess_type(filename)[0]
    print('mime: ',mime, type(mime))

    # get file extension bc mimetype sucks sometimes
    extension = filename.split(".")[-1]
    print('extension: ',extension , type(extension))

    a = {
        "username": "me",
        "cookie": "test_cookie",
        "chatroom": "conv1",
        "type": "file",
        "mimetype": mime,
        "extension": extension
    }

    # streaming uploads like this make it so the file is never fully loaded into memory
    # im sorry but this one thing will change a lot, but ill probably make a function that is a drop in replacement and you wont have to bother with it
    print(a)
    with open(filename, 'rb') as f:
        data = f.read()
    res = requests.post(url, json=a)


    print(res.text)
