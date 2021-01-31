import requests
import json
import base64

# local
import helper


def encode(a):
    return base64.b64encode(a.encode('utf-8')).decode('utf-8')
def encode_binary(a):
    return base64.b64encode(a).decode('utf-8')



def get(s, username):
    url = "http://localhost:5000/api/v0/message/"

    headers = {
        "username": username,
        "time": "1604951915.377928",
        "chatroom": "conv1",
    }


    res = s.get(url=url, headers=headers)

    print(res.text)
    #print(base64.b64decode(res.text).decode('utf-8'))


def send_file(s, username):
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
        "username": username,
        "chatroom": "conv1",
        "type": 'file',
        'extension': extension,
        'data': contents
            }

    res = s.post(url=url, json=a)

    return res.text



def send_message(s, username):
    url = "http://localhost:5000/api/v0/message/"

    message = input(">> ")

    a = {
        "username": username,
        "nickname": "bruh",
        "type": "text",
        "chatroom": "conv1",
        "message": encode(message)
    }

    res = s.post(url, json=a)


    return res.text


def get_file(s, username):
    url = "http://localhost:5000/api/v0/file/"

    headers = {
            "username": username,
            "filename": input(">> "),
            "chatroom": 'conv1'
            }

    res = s.get(url=url, headers=headers)

    return res.text



def login(s):
    url = "http://localhost:5000/login"

    a = {
        "username": input("username: "),
        "password" : input("password: ")
    }

    res = s.post(url=url, json=a)
    print(res.text)
    print(res.cookies)
    return s, a['username']


def register(s):
    url = "http://localhost:5000/register"

    a = {
        "username": input("username: "),
        "email": input("email: "),
        "nickname": input("nickname: "),
        "password" : input("password: ")
    }

    res = s.post(url=url, json=a)
    print(res.text)
    return s




s = requests.Session()
cookies = ''
username = ''
while 1:
    
    print("cookies: ", s.cookies)

    choice = input('type: ')
    if choice == 'sfile':
        print(send_file(s, username))
    if choice == 'gfile':
        print(get_file(s, username))
    elif choice == 'send':
        print(send_message(s, username))
    elif choice == 'get':
        print(get(s, username))
    elif choice == 'logout':
        s = requests.Session()
    elif choice == 'register':
        s = register(s)
    elif choice == 'login':
        s, username = login(s)

