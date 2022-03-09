"""
api.py -- should come up with a better name for this.


This module serves one purpose. That is not cluttering up the
main file too much. Each method in the main file directly
calls one of the functions here, which then actually make things happen.
"""

import json
import codectrl
import logging
import coloredlogs


import th__helpers as helpers
import th__security as security
import th__filesystem as filesystem
from th__database import Database



def create_chatroom(request) -> tuple[dict[str, str | int], int]:
    """ Create a new chat-room """

    username: str       = request.get_json().get('username')
    nickname: str       = request.get_json().get('nickname')
    password: str       = request.get_json().get('password')
    chatroom_name: str  = request.get_json().get('chatroom-name')


    # The nickname argument is optional and if not set it will be the same as username.
    nickname = (nickname if nickname is not None else username)


    # Make sure all arguments are not None
    required = ['username', 'password', 'chatroom_name']
    for i, req in enumerate([username, password, chatroom_name]):
        if req is None or len(req) < 1:
            return {"error": f"No value supplied for required field: {required[i]}"}, 400


    # Make sure all are strings, and an acceptable length
    if not isinstance(username, str) or len(username) < 1 or len(username) > 20:
        return {"error": "Username has to be a string between 1 and 20 characters."}, 400
    if not isinstance(nickname, str) or len(nickname) < 1 or len(nickname) > 20:
        return {"error": "Nickname has to be a string between 1 and 20 characters."}, 400


    # Password needs some extra checks as it has to meet the
    # minimum length requirements
    min_password_length = 10 # Check server settings for this
    if not isinstance(password, str) or len(password) < min_password_length or len(password) > 100:
        return {
            "error": f"Password has to be a string between\
                      {min_password_length} and 100 characters."
        }, 400


    # Create a new UUID for the chat-room.
    chatroom_id: str = security.gen_uuid()


    # Create folders needed for chatroom
    res, status = filesystem.create_chatroom_folders(chatroom_id)
    if helpers.bad(status):
        return res, status


    # Create the database for the chatroom
    db_class = Database(chatroom_id, username, password, nickname)
    return db_class.init_chatroom(chatroom_name)
