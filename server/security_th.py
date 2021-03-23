# this file is for sanitization, ecryption and etc
    # some functions seem small but are here for modularity purposes
import os
import uuid
import base64
import bcrypt
import string
from hashlib import sha256

from logging_th import logger as log

# base64 encode messages
def encode(a):
    return base64.b64encode(str(a).encode('utf-8')).decode('utf-8')

# base64 decode messages
def decode(a):
    return base64.b64decode(str(a).encode('utf-8')).decode('utf-8')


def sanitize_uuid(ID):
    log(level='warning', msg="sanitize_uuid is now depricated and should be replaced with check_uuid")
    ID = str(ID)
    ID = ID.replace('..', '')
    ID = ID.replace('/', '')

    if len(ID) != 36:
        print('ID: ',ID , len(ID))
        return False

    # validate uuid:
    try:
        uuid.UUID(ID).version
    except ValueError as e:
        print('ID: ',ID , type(ID))
        return False


    return ID


def check_uuid(ID):
    ID = str(ID)
    allowed = string.digits + string.ascii_letters + '-'

    for i in ID:
        p = allowed.find(i)
        if p < 0:
            print('ID: ',ID , len(ID))
            return f"[security/check_uuid/0] || Invalid or dangerous uuid send from user. Cannot contain: '{i}'", 400


    if len(ID) != 36:
        print('ID: ',ID , len(ID))
        return f"[security/check_uuid/1] || Invalid uuid send from user. UUID length must equal to 36", 400

    # validate uuid:
    try:
        uuid.UUID(ID).version
    except ValueError as e:
        print('ID: ',ID , type(ID))
        return f"[security/check_uuid/3] || Invalid or dangerous uuid send from user. Not a UUID!", 400


    return ID, 200


def sanitize_chatroomId(chatroom_id):
    try:
        chatroom_id = str(chatroom_id)
        chatroom_id = chatroom_id.replace('..', '')
        chatroom_id = chatroom_id.replace('/', '')
    except Exception as e:
        return "invalid chatroom_id", 400


    # validate uuid:
        # commented out because chatroom_id's are not uuids YET
    #try:
    #    uuid.UUID(uuid).version
    #except ValueError:
    #    return "invalid chatroom id", 400

    return chatroom_id, 200


# yes this is overly simple but lets me control all uuids in one place
def gen_uuid():
    cookie = str(uuid.uuid1())
    return cookie


def hashpw(password):
    password = password.encode("utf-8")
    password = bcrypt.hashpw(password, bcrypt.gensalt(rounds=16))
    return password.decode("utf-8")



# uses bcrypt to check a password
def checkpw(password, storedPassword):
    password = password.encode("utf-8")
    storedPassword = storedPassword.encode("utf-8")
    return bcrypt.checkpw(password, storedPassword)



