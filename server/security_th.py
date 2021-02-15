# this file is for sanitization, ecryption and etc
    # some functions seem small but are here for modularity purposes
import os
import uuid
import bcrypt
from hashlib import sha256

from logging_th import logger as log

def sanitize_filename(filename):
    filename = filename.replace('..', '')
    filename = filename.replace('/', '')

    if len(filename) != 36:
        return "invalid filename length", 400

    # validate uuid:
    try:
        uuid.UUID(filename).version
    except ValueError:
        return "invalid filename", 400


    return filename, 200



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


# yes this is overly simple, and yes its like this bc im pretty sure it wont be this simple for long
def generate_cookie():
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



