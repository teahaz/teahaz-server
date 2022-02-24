"""
    This module has all security related functions
    like password hashes, UUID's and other filtering
    functions.

    The goal of this is that we can replace the way
    something is verified or hashed in one place
    rather than making sure its changed everywhere.
"""

import uuid
import string


def is_uuid(uid: str) -> bool:
    """ Function verifies if string is a valid UUID """
    uid = str(uid)

    # UUID's can only contain hexdigits and hyphens
    for char in uid:
        if char not in string.hexdigits + '-':
            return False

    try:
        uuid.UUID(uid).version
    except NameError:
        return False

    return True




def gen_uuid():
    """
        Generates uuid.

        This is its own function so it can be
        be changed in one place if need be.
    """
    return str(uuid.uuid1())
