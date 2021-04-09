import requests
import time
import os
import json
import string
import base64
import teahaz


def encode(a):
    return base64.b64encode(a.encode('utf-8')).decode('utf-8')
def encode_binary(a):
    return base64.b64encode(a).decode('utf-8')


def sanitize_filename(a):
    allowed = string.ascii_letters + string.digits + '_-.'
    a = a.replace('..', '_')

    filename = ''
    for i in a:
        if i not in allowed:
            i = '_'
        filename += i

    return filename

global s
global url
global username
global chatroom_id
# url = "http://butorhaz.hopto.org:13337"
# url = "https://butorhaz.hopto.org"
url = "http://localhost:13337"
# url = "http://localhost:80"
# url = "https://teahaz.co.uk"
# url = "http://192.168.1.75"



def send_file():
    url = globals()['url'] + "/api/v0/file/" + globals()['chatroom_id']

    # get filename from user
    filepath = input(">> ")
    print('filepath: ',filepath , type(filepath))

    if not os.path.exists(filepath):
        return "sorry this file doesnt exist"

    # get file extension bc mimetype sucks sometimes
    filename = filepath.split("/")[-1]
    filename = sanitize_filename(filename)


    # get length of file
    f = open(filepath, 'ab+')
    length = f.tell()
    print('length: ',length , type(length))
    f.close()


    # set chunk size
    chunk_size = int((1048576*3)/4) -1

    # response, status_code = teahaz.upload_file_v0(globals()['s'], globals()['url'], globals()['chatroom_id'], globals()['username'], filepath, filename)
    f = open(filepath, "rb")

    fileId = input('fileId: ')
    if len(fileId) < 33:
        fileId = None

    last = False
    while not last:
        c = f.read(chunk_size)


        # check if this will be the last part
        if len(c) < chunk_size or f.tell() >= length:
            last = True


        data = {
                "username" : globals()['username'],
                "filename" : filename, 
                "fileId"   : fileId,
                "type"     : 'file',
                "last"     : last,
                "data"     : encode_binary(c),
                "kId"      : None
                }


        # make request
        response = globals()['s'].post(url, json=data)
        if response.status_code != 200:
            break
        else:
            print("text")
            print(response.text)
            fileId = response.json().get('fileId')
            print("fileID")
            print(fileId)

    f.close()
    # return the response if the loop stopped
    return response.text, response.status_code


def get_file():
    filename = input(">> ")
    saved_filename = input("save as: ")


    # response, status_code = teahaz.download_file_v0(globals()['s'], globals()['url'], globals()['chatroom_id'], globals()['username'], filename, saved_filename)

    # print(status_code)
    # return response



def get():
    url = globals()['url'] + "/api/v0/message/" + globals()['chatroom_id'] + '/'

    headers = {
        "username": globals()['username'],
        "time": "1604951915.377928"
    }


    res = globals()['s'].get(url=url, headers=headers)

    print("status_code: ", res.status_code)
    print(res.text)


def gid():
    url = globals()['url'] + "/api/v0/message/" + globals()['chatroom_id'] + '/'

    headers = {
        "username": globals()['username'],
        "messageId": input('id >>')
    }


    res = globals()['s'].get(url=url, headers=headers)

    print("status_code: ", res.status_code)
    print(res.text)


def delete():
    url = globals()['url'] + "/api/v0/message/" + globals()['chatroom_id'] + '/'

    a = {
        "username": globals()['username'],
        "messageId": input('id>> ')
    }


    res = globals()['s'].delete(url=url, json=a)

    print("status_code: ", res.status_code)
    print(res.text)


def send_message():
    url = globals()['url'] + "/api/v0/message/" + globals()['chatroom_id'] +'/'

    message = input(">> ")

    a = {
        "username": globals()['username'],
        "type": "text",
        "message": encode(message)
    }

    res = globals()['s'].post(url, json=a)
    print("status_code: ", res.status_code)

    return res.text


def send_n():
    url = globals()['url'] + "/api/v0/message/"

    message = "\x0a"

    a = {
        "username": globals()['username'],
        "type": "text",
        "chatroom": globals()['chatroom_id'],
        "message": encode(message)
    }

    res = globals()['s'].post(url, json=a)
    print("status_code: ", res.status_code)

    return res.text



def login():
    url = globals()['url'] + "/login/" + globals()['chatroom_id']

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
    url = globals()['url'] + "/login/"+globals()['chatroom']

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
    url = globals()['url'] + "/api/v0/chatroom/"

    globals()['username'] = input("username: ")
    a = {
            "username": globals()['username'],
            "email": input("email: "),
            "nickname": input("nickname: "),
            "password" : input("password: "),
            "chatroom_name": input("chatroom_name: ")
            }

    res = globals()['s'].post(url=url, json=a)
    if res.status_code == 200:
        globals()['chatroom_id'] = json.loads(str(res.text).strip('\n').strip('"')).get('chatroom')

    return res.text



def get_chatroms():
    url = globals()['url'] + "/api/v0/chatroom/"

    a = {
            "username": globals()['username'],
            }

    res = globals()['s'].get(url=url, headers=a)

    return res.text


def get_invite():
    url = globals()['url']

    expr_time = 0
    uses =  str(int(input("uses: "))).strip('\n')

    response, status_code = teahaz.create_invite_v0(globals()['s'], url, globals()['chatroom_id'], globals()['username'], expr_time, uses)
    if status_code == 200:
        print("invite: ", str(response).strip('\n').strip('"'))

    return response, status_code


def bazsitest():
    a = {
            'User-Agent': 'teahaz.py-v0.0', 
            'email': "sf",
            'username': 'j',
            'nickname': ':robot:johnny:robot:',
            'password': '1234567890',
            'inviteId': "21969daa-9127-11eb-a89b-0242ac110002"
            }
    url = 'https://teahaz.co.uk/api/v0/invite/1714e1a8-87ee-11eb-931c-0242ac110002'

    res = globals()['s'].post(url=url, json=a)
    print(res.text)


def use_invite():
    globals()['chatroom'] = input("chatroom: ")
    globals()['username'] = input("username: ")
    globals()['email'] = input("email: ")
    url = globals()['url'] + "/api/v0/invite/"+globals()['chatroom']

    a = {

            "username": globals()['username'],
            "nickname": "\x0aB\x0a",
            "email": globals()['email'],
            # "nickname": input('nickname: '),
            "password": input('password: '),
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
    elif choice == 'gid':
        print(gid())
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
    elif choice == 'del':
        print(delete())
    elif choice == 'biz':
        print(bazsitest())

    print("username: ", globals()['username'])
    print("chatroom_id: ", globals()['chatroom_id'])

