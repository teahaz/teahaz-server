"""
    This module does things on the filesystem.

    No function outside this module should ever
    touch the filesystem in any way.
"""

import os
import logging
import codectrl
import th__security as security



def chatroom_directories_exist(chatroom_id: str) -> bool:
    """ Check if chatroom_id is valid, and that it exists on disk """

    if not security.is_uuid(chatroom_id):
        return False
    if not os.path.exists(f'storage/chatrooms/{chatroom_id}'):
        return False
    return True




def create_chatroom_folders(chatroom_id: str) -> tuple[dict, int]:
    """
        Create a directory for each chatroom.

        The directory will store all uploaded
        files for the chat-room, along side anything
        else that needs disc storage in the future.
    """

    # Can't have weird filenames
    if not security.is_uuid(chatroom_id):
        return {"error": "Invalid UUID!"}, 400


    # Make sure the chatrooms storage folder exists.
    # If it doesn't then something is very wrong.
    if not os.path.exists("storage/chatrooms/"):
        logging.error("The storage/chatrooms folder does not exist.")
        return {"error": "Internal server error: The chatroom storage folder does not exist"}, 500


    # Don't create a chat-room if it already exits
    if os.path.exists(f"storage/chatrooms/{chatroom_id}"):
        return {"error:": "Chatroom already exists"}, 400


    try:
        os.mkdir(f'storage/chatrooms/{chatroom_id}')
        os.mkdir(f'storage/chatrooms/{chatroom_id}/uploads')

    except Exception as err: # pylint: disable=broad-except
        logging.error("Failed to create chatroom folders: %s", err)
        return {"error": "Internal server error: Failed to create directories for chatroom."}, 500

    return {}, 200
