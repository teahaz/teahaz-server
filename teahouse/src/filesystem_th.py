"""
    This file is responsible for handling all filesystem operations.
"""

import os
import time
import shutil
import security_th as security


# setup logging
from logging_th import logger
LOG = logger()

def _create_folders():
    try:
        if not os.path.exists('storage'):
            os.mkdir('storage')

        if not os.path.exists('storage/chatrooms'):
            os.mkdir('storage/chatrooms')

        return "OK", 200

    except Exception as e:
        LOG.error(_create_folders, "Failed to create storage folders!")
        return "Internal server error while setting up storage folders.", 500


def create_chatroom_folders(chatroomID):
    """ Create chatroom folders on disc """
    if not security.is_uuid(chatroomID):
        return "Invalid uuid", 400

    # make sure storage folders exist
    res, status = _create_folders()
    if status != 200:
        return res, status


    if os.path.exists(f"storage/chatrooms/{chatroomID}"):
        return "Internal server error: cannot recreate existing chatroom", 400

    try:
        os.mkdir(f'storage/chatrooms/{chatroomID}')
        os.mkdir(f'storage/chatrooms/{chatroomID}/uploads')

        # NOTE this is no longer needed and just keeping to not crash while we migrate
        open(f"storage/chatrooms/{chatroomID}/main.db", "w+").close()

    except Exception as e:
        LOG.error(create_chatroom_folders, f"Failed to create chatroom folders! Traceback: {e}")
        return f"Internal server error: failed while setting up the chatroom", 500

    return "OK", 200




def remove_chatroom(chatroomID):
    """ Remove chatroom folders from disc """
    if not security.is_uuid(chatroomID):
        return "Invalid uuid", 400

    try:
        shutil.rmtree(f'storage/chatrooms/{chatroomID}', ignore_errors=True)

    except Exception as e:
        LOG.error(remove_chatroom, f"Failed to remove chatroom folders\n Traceback: {e}")
        return "Failed to remove chatroom folders", 500

    return "OK", 200




def chatroom_exists(chatroomID):
    """ Check if chatroomID is valid, and that it exists on disc """

    if not security.is_uuid(chatroomID): return False
    if not os.path.exists(f'storage/chatrooms/{chatroomID}'): return False
    return True
