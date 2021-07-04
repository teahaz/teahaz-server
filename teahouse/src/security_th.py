import os
import uuid
import base64
import bcrypt
import string
from hashlib import sha256


def encode(a):
    " base64 encode "
    return base64.b64encode(str(a).encode('utf-8')).decode('utf-8')

def decode(a):
    " base64 decode "
    return base64.b64decode(str(a).encode('utf-8')).decode('utf-8')



def gen_uuid():
    """
        Generates uuid.

        This is done centrally because it makes it easy to change later.
    """

    cookie = str(uuid.uuid1())
    return cookie



def hashpw(password: str):
    """ bcrypt hash password for storage """
    password = password.encode("utf-8")
    password = bcrypt.hashpw(password, bcrypt.gensalt(rounds=16))
    return password.decode("utf-8")

def checkpw(password: str, hashedpw: str):
    """ Compare hashed password with real one to check if they are the same """
    password = password.encode("utf-8")
    hashedpw = hashedpw.encode("utf-8")
    return bcrypt.checkpw(password, hashedpw)



def is_uuid(uid: str) -> bool:
    uid = str(uid)

    for i in uid:
        if i not in string.hexdigits + '-':
            return False

    try:
        uuid.UUID(uid).version
    except ValueError as e:
        return False

    return True


