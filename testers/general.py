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

        "userId": "1234567890",
        "nickname": "bruh",
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
        "userId": "1234567890",
        "nickname": "bruh",
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
        "userId": "1234567890",
        "nickname": "bruh",
        "type": "text",
        "chatroom": "conv1",
        "message": encode(message)
    }

    res = s.post(url, json=a)


    return res.text


def get_file(s):
    url = "http://localhost:5000/api/v0/file/"

    headers = {
            "userId": "1234567890",
            "nickname": "bruh",
            "filename": input(">> "),
            "chatroom": 'conv1'
            }

    res = s.get(url=url, headers=headers)

    return res.text



def login(s):
    url = "http://localhost:5000/login"

    a = {
        "userId": input("username: "),
        "password" : input("password: ")
    }

    res = s.post(url=url, json=a)
    print(res.text)
    print(res.cookies)
    return s


def register(s):
    url = "http://localhost:5000/register"

    a = {
        "nickname": input("username: "),
        "password" : input("password: ")
    }

    res = s.post(url=url, json=a)
    print(res.text)
    return s




s = requests.Session()
cookies = ''
s = login(s)
while 1:
    
    print("cookies: ", s.cookies)

    choice = input('type: ')
    if choice == 'sfile':
        print(send_file(s))
    if choice == 'gfile':
        print(get_file(s))
    elif choice == 'send':
        print(send_message(s))
    elif choice == 'get':
        print(get(s))
    elif choice == 'remove':
        # remove cookies
        s = requests.Session()
    elif choice == 'register':
        s = register(s)

