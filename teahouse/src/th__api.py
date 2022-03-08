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


    # Create a new UUID for the chat-room.
    chatroom_id: str = security.gen_uuid()


    # Create folders needed for chatroom
    res, status = filesystem.create_chatroom_folders(chatroom_id)
    if status != 200:
        return res, 500



