import requests
import json
import base64

# local
import helper


def encode(a):
    return base64.b64encode(a.encode('utf-8')).decode('utf-8')
def encode_binary(a):
    return base64.b64encode(a).decode('utf-8')



def get(s):
    url = "http://localhost:5000/api/v0/message/"

    headers = {

        "username": "bruh",
        "cookie": "AAAA",
        "time": "1604951915.377928",
        "chatroom": "conv1",
    }


    res = s.get(url=url, headers=headers)

    print(res.text)
    #print(base64.b64decode(res.text).decode('utf-8'))


def send_file(s):
    url = "http://localhost:5000/api/v0/file/"
    # get filename from user
    filename = input(">> ")

    # this is just so i can test without typing a filename each time
    if len(filename) == 0:
        filename = '../notes.md'
    print(filename)


    with open(filename, 'rb')as infile:
        contents = infile.read()

    contents = encode_binary(contents)

    # get file extension bc mimetype sucks sometimes
    extension = filename.split(".")[-1]
    print('extension: ',extension , type(extension))


    a = {
        "username": "me",
        "cookie": "test_cookie",
        "chatroom": "conv1",
        "type": 'file',
        'extension': extension,
        'data': contents
            }

    res = s.post(url=url, json=a)

    return res.text



def send_message(s):
    url = "http://localhost:5000/api/v0/message/"

    message = input(">> ")

    a = {
        "username": "me",
        "cookie": "test_cookie",
        "type": "text",
        "chatroom": "conv1",
        "message": encode(message)
    }

    res = s.post(url, json=a)


    return res.text


def get_file(s):
    url = "http://localhost:5000/api/v0/file/"

    headers = {
            "username": 'me',
            "filename": input(">> "),
            "chatroom": 'conv1'
            }

    res = s.get(url=url, headers=headers)

    return res.text

s = requests.Session()
while 1:
    choice = input('type: ')
    if choice == 'sfile':
        print(send_file(s))
    if choice == 'gfile':
        print(get_file(s))
    elif choice == 'send':
        print(send_message(s))
    elif choice == 'get':
        print(get(s))

