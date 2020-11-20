import requests
import json
import base64

# local
import helper


def b(a):
    return base64.b64encode(a.encode('utf-8')).decode('utf-8')



def get(s):
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


def send_file(s):
    url = "http://localhost:5000/api/v0/file/"

    filename = input(">> ")

    # this is just so i can test without typing a filename each time
    if len(filename) == 0:
        filename = '../notes.md'
    print(filename)



    a = {
        "username": "me",
        "cookie": "test_cookie",
        "chatroom": "conv1",
    }

    res = helper.sendfile(url, a, filename)

    return res.text



def send_message(s):
    url = "http://localhost:5000/api/v0/message/"

    message = input(">> ")

    a = {
        "username": "me",
        "cookie": "test_cookie",
        "type": "text",
        "chatroom": "conv1",
        "message": b(message)
    }

    res = requests.post(url, json=a)

    return res.text






s = requests.Session()
while 1:
    choice = input('type: ')
    if choice == 'sfile':
        print(send_file(s))
    elif choice == 'send':
        print(send_message(s))
    elif choice == 'get':
        print(get(s))

