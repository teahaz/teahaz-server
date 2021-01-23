# this file handles all things connected to local files
import os
from logging_th import logger as log

def save_file(data, chatroom, extension, filename):
    # uuid is used as a filename
    # this way we limit string escape and filesystem related vulnerabilities

    # this should only happen if someone modified the server, TODO: should call a function/fix to redifine the chatroom
    if not os.path.exists(f'storage/{chatroom}/uploads'):
        log(level='error', msg=f'[server/helpers/save_file/0] uploads forlder does not exist for chatroom:  {chatroom}')
        # if chatroom re init is called here then just move on and dont return
        # if it attempts to fix this thent his should only return on an unsuccessful fix
        return False


    try:
        # write file if possible
        # data is in text form so it doesnt need to be written in binary
        with open(f'storage/{chatroom}/uploads/{filename}', 'w')as outfile:
            outfile.write(data)

    except Exception as e:
        # if that failed log it, with the exeption
        log(level='error', msg=f'failed to write file: storage/{chatroom}/uploads/{filename}   exeption: {e}')
        return False


    # file was saved successfully
    return True





def read_file(chatroom, filename):
    try:
        with open(f'storage/{chatroom}/uploads/{filename}', 'r')as infile:
            data = infile.read()
    except:
        return False
    return data

