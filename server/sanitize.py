from server_logger import logger as log

def filename(filename):
    filename = filename.replace('..', '')
    filename = filename.replace('/', '')

    if len(filename) != 36:
        log(level='warning', msg=f'user supplied a filename with and invalid lenght, pls make sure that te filename is 36bytes long')
        return False

    return filename


def chatroom(chatroom_id):
    chatroom_id = chatroom_id.replace('..', '')
    chatroom_id = chatroom_id.replace('/', '')
    return chatroom_id
