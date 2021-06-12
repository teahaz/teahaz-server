import os
import uuid
import base64
import bcrypt
import string
from hashlib import sha256


def encode(a):
    " base64 encode "
    return base64.b64encode(str(a).encode('utf-8')).decode('utf-8')

# base64 decode messages
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
