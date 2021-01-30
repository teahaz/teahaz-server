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
        log(level='warning', msg=f'user supplied a filename with and invalid lenght, pls make sure that te filename is 36bytes long')
        return False

    return filename



def sanitize_chatroomId(chatroom_id):
    chatroom_id = chatroom_id.replace('..', '')
    chatroom_id = chatroom_id.replace('/', '')
    return chatroom_id


# yes this is overly simple, and yes its like this bc im pretty sure it wont be this simple for long
def generate_cookie():
    cookie = str(uuid.uuid1())
    return cookie

# yes this is overly simple, and yes its like this bc im pretty sure it wont be this simple for long
def generate_userId():
    userId = str(uuid.uuid1())
    return userId



def hashpw(password):
    password = password.encode("utf-8")
    password = bcrypt.hashpw(password, bcrypt.gensalt(rounds=16))
    return password.decode("utf-8")



# uses bcrypt to check a password
def checkpw(password, storedPassword):
    password = password.encode("utf-8")
    storedPassword = storedPassword.encode("utf-8")
    return bcrypt.checkpw(password, storedPassword)



