# this file handles all things connected to local files
import os
import shutil
from logging_th import logger as log

def save_file(data, chatroom, extension, filename):
    if not os.path.exists(f'storage/{chatroom}/uploads'): # make sure uploads folder exists
        log(level='error', msg=f'[server/filesystem_th/save_file/0] uploads forlder does not exist for chatroom:  {chatroom}')
        return "internal server error while saving file", 500


    # save file
    try:
        with open(f'storage/{chatroom}/uploads/{filename}', 'w')as outfile:
            outfile.write(data)


    # failed to save file
    except Exception as e:
        log(level='error', msg=f'failed to write file: storage/{chatroom}/uploads/{filename}   exeption: {e}')
        return "internal server error while saving file", 500


    # all is well
    return "OK", 200


def read_file(chatroom, filename):
    try:
        # as all files are base64 encoded text files, they can all be read without 'b'
        with open(f'storage/{chatroom}/uploads/{filename}', 'r')as infile:
            data = infile.read()
    except:
        return "Internal server error", 500

    # all is well
    return data, 200


def remove_file(chatroom, filename):
    try: # remove file
        os.remove(f'storage/{chatroom}/{filename}')
    except:
        return "internal server error while removeing file", 500


    # all is well
    return "OK", 200


def create_chatroom_folders(chatroomId):
    if os.path.exists(f"storage/{chatroomId}"):
        return "chatroomId already exists", 400

    try:
        os.mkdir(f'storage/{chatroomId}')
        os.mkdir(f'storage/{chatroomId}/uploads')

    except Exception as e:
        return f"failed to create chatroom folders: {e}", 500

    return "OK", 200


def remove_chatroom(chatroom):
    try:
        shutil.rmtree(f'storage/{chatroom}', ignore_errors=True)


    except Exception as e:
        log(level='error', msg=f"[server/filehanler/remove_chatroom/0] could not remove chatroom\n Traceback: {e}")
        return "could not remove the chatroom", 500


    return "OK", 200
