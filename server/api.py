import time
import base64
import json

import helpers
from helpers import decode_messages as d



def message_send(json_data):
    # get the data needed for this function
    username = json_data['username']
    cookie = json_data['cookie']
    message_type = json_data['type']
    chatroom_id = json_data['chatroom']
    message = json_data['message']

    # check message type
    if not message_type == "text":
        return 400, "posting non-'text' type to /message is forbidden"

    # authenticate
    if not helpers.authenticate(username , cookie):
        return 401, "not authenticated"

    # check chatroom permission
    if not helpers.check_access(username , chatroom_id):
        return 401, "chatroom doesnt exist or user doesnt have access to view it"

    # store message that got sent
    response = helpers.save_message(
            time=time.time(),
            username=username,
            chatroom_id = chatroom_id,
            message=message
            )

    return 200, response






def message_get(json_data):
    #username = json_data['username']
    #cookie = json_data['cookie']
    #last_time = json_data['last_get_time']
    #convId = json_data['convId']

    # checks if user is authenticated
    #if not helpers.authenticate(username, cookie): return 401, "unauthorized"
    ##check if conversation exists, and if user has permission
    #if not helpers.is_valid_chatroom(convId, username, cookie): return 403, "chatroom doesnt exist or not authorized"


    #print(d(username), d(cookie), d(last_time), d(convId))
    #return 200, json_data
    return 200, ''



def upload_file(json_data):
    return 200, 'filename'



def download_file(json_data):
    return 200, 'filename'
