"""
    This file is responsible for handling all filesystem operations.
"""

import os
import time
import shutil
import security_th as security


# setup logging
from logging_th import logger
global log
log = logger()


def create_chatroom_folders(chatroomID):
    """ Create chatroom folders on disc """
    if os.path.exists(f"storage/{chatroomID}"):
        return "Internal server error: tried to assing existing chatroom ID", 400

    try:
        os.mkdir(f'storage/chatrooms/{chatroomID}')
        os.mkdir(f'storage/chatrooms/{chatroomID}/uploads')
        a = open(f"storage/chatrooms/{chatroomID}/main.db", "w+")
        a.close()

    except Exception as e:
        log.error(create_chatroom_folders, f"Failed to create chatroom folders! Traceback: {e}")
        return f"Internal server error: failed while setting up the chatroom", 500

    return "OK", 200




def remove_chatroom(chatroomID):
    """ Remove chatroom folders from disc """
    try:
        shutil.rmtree(f'storage/chatrooms/{chatroomID}', ignore_errors=True)

    except Exception as e:
        log.error(remove_chatroom, f"Failed to remove chatroom folders\n Traceback: {e}")
        return "Failed to remove chatroom folders", 500

    return "OK", 200
