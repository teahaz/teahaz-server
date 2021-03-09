# this file is for sanitization, ecryption and etc
    # some functions seem small but are here for modularity purposes
import os
import uuid
import bcrypt
from hashlib import sha256

from logging_th import logger as log

def sanitize_uuid(ID):
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



