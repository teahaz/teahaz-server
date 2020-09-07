import base64

# check if requested chatroom exists, and if the user is authorized to look at it
def is_valid_chatroom(convId, username, cookie):
    return True


def authenticate(usrname, cookie):
    return True


def decode_messages(data):
    return base64.b64decode(data).decode('utf-8')

