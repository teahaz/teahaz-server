import requests
import time
import os
import json
import base64


def encode(a):
    return base64.b64encode(a.encode('utf-8')).decode('utf-8')
def encode_binary(a):
    return base64.b64encode(a).decode('utf-8')


global s
global url
global username
global chatroom_id
#url = "http://butorhaz.hopto.org:13337"
url = "http://localhost:13337"

def get():
    url = globals()['url'] + "/api/v0/message/"

    headers = {
        "username": globals()['username'],
        "time": "1604951915.377928",
        "chatroom": globals()['chatroom_id'],
    }


    res = globals()['s'].get(url=url, headers=headers)

    print("status_code: ", res.status_code)
    print(res.text)


def send_file():
    url = globals()['url'] + "/api/v0/file/"

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
        "username": globals()['username'],
        "chatroom": globals()['chatroom_id'],
        "type": 'file',
        'extension': extension,
        'data': contents
            }

    res = globals()['s'].post(url=url, json=a)

    print("status_code: ", res.status_code)
    return res.text



def send_message():
    url = globals()['url'] + "/api/v0/message/"

    message = input(">> ")

    a = {
        "username": globals()['username'],
        "type": "text",
        "chatroom": globals()['chatroom_id'],
        "message": encode(message)
    }

    res = globals()['s'].post(url, json=a)
    print("status_code: ", res.status_code)

    return res.text



def get_file():
    url = globals()['url'] + "/api/v0/file/"

    headers = {
            "username": globals()['username'],
            "filename": input(">> "),
            "chatroom": globals()['chatroom_id']
            }

    res = globals()['s'].get(url=url, headers=headers)


    return res.text



def login():
    url = globals()['url'] + "/login/"

    choice = input("login with email or username? [e/u]")

    if 'E' in choice.upper():
        a = {
            "email": input("email: "),
            "password" : input("password: ")
        }
    else:
        a = {
            "username": input("username: "),
            "password" : input("password: ")
        }

    if a.get('username'):
        globals()['username'] = a.get('username')
    else:
        globals()['username'] = input("you logged in with email, but my shitty client needs a username to work.\npls give username: ")

    res = globals()['s'].post(url=url, json=a)
    print(res.text)
    print(res.cookies)
    return s, username



def clogin():
    url = globals()['url'] + "/login/"

    a = {
        "username": globals()['username'],
    }

    res = globals()['s'].get(url=url, headers=a)

    return res.text



def register():
    url = globals()['url'] + "/register/"

    a = {
        "username": input("username: "),
        "email": input("email: "),
        "nickname": input("nickname: "),
        "password" : input("password: ")
    }

    res = globals()['s'].post(url=url, json=a)
    print(res.text)
    return s



def create_chatroom():
    url = globals()['url'] + "/api/v0/chatrooms/"

    a = {
            "username": globals()['username'],
            "chatroom_name": input("chatroom_name: ")
            }

    res = globals()['s'].post(url=url, json=a)
    if res.status_code == 200:
        globals()['chatroom_id'] = str(res.text).strip('\n').strip('"')

    return res.text



def get_chatroms():
    url = globals()['url'] + "/api/v0/chatrooms/"

    a = {
            "username": globals()['username'],
            }

    res = globals()['s'].get(url=url, headers=a)

    return res.text


def get_invite():
    url = globals()['url'] + "/api/v0/invite/"

    a = {

            "username": globals()['username'],
            "chatroom": globals()['chatroom_id'],
            "expr_time": str(time.time() + 60 * 60 * 24),
            "uses": str(10)
            }

    res = globals()['s'].get(url=url, headers=a)
    if res.status_code == 200:
        print("invite: ", str(res.text).strip('\n').strip('"'))

    return res.text


def use_invite():
    url = globals()['url'] + "/api/v0/invite/"

    a = {

            "username": globals()['username'],
            "chatroom": input("chatroom: "),
            "inviteId": input("invite: ")
            }

    res = globals()['s'].post(url=url, json=a)
    return res.text


s = requests.Session()
cookies = ''
username = ''
chatroom_id = ''
while 1:
    print("cookies: ", s.cookies)

    choice = input('type: ')
    if choice == 'sfile':
        print(send_file())
    if choice == 'gfile':
        print(get_file())
    elif choice == 'send':
        print(send_message())
    elif choice == 'get':
        print(get())
    elif choice == 'logout':
        s = requests.Session()
    elif choice == 'register':
        s = register()
    elif choice == 'login':
        s, username = login()
    elif choice == 'clogin':
        print(clogin())
    elif choice == 'newchat':
        print(create_chatroom())
    elif choice == 'getchats':
        print(get_chatroms())
    elif choice == 'chat':
        globals()['chatroom_id'] = input('chatroom: ')
    elif choice == 'ginvite':
        print(get_invite())
    elif choice == 'uinvite':
        print(use_invite())

    print("username: ", globals()['username'])
    print("chatroom_id: ", globals()['chatroom_id'])

