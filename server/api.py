import time
import json
import base64

import helpers


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

    return 200, str(response)






def message_get(json_data):
    username = json_data['username']
    cookie = json_data['cookie']
    last_time = json_data['time']
    chatroom_id = json_data['chatroom']

    ## pls make sure to error check this
    last_time = int(last_time)

    # checks if user is authenticated
    if not helpers.authenticate(username, cookie):
        return 401, "unauthorized"

    # check chatroom permission
    if not helpers.check_access(username , chatroom_id):
        return 401, "chatroom doesnt exist or user doesnt have access to view it"


    return_data = helpers.get_messages(last_time=last_time, chatroom_id=chatroom_id)

    #print(d(username), d(cookie), d(last_time), d(convId))
    return 200, return_data




def upload_file(json_data):
    return 200, 'filename'



def download_file(json_data):
    return 200, 'filename'
