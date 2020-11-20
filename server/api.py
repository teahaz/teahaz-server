# modules
import uuid
import time
import json
import base64

# local
import helpers



def message_send(json_data):
    # get the data needed for this function
    username = json_data['username']
    cookie = json_data['cookie']
    chatroom_id = json_data['chatroom']
    message_type = json_data['type']

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
    if not helpers.save_in_db(
            time=time.time(),
            username=username,
            chatroom_id = chatroom_id,
            message_type='text',
            message=message
            ):
        return 500, "server failed to save mesage"

    return 200, "OK"




def message_get(json_data):
    username = json_data['username']
    cookie = json_data['cookie']
    chatroom_id = json_data['chatroom']

    last_time = json_data['time']

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
    username = json_data['username']
    cookie = json_data['cookie']
    chatroom_id = json_data['chatroom']
    message_type = json_data['type']

    data = json_data['data']
    mime_type = json_data['mimetype']
    extension = json_data['extension']

    # check message type
    if not message_type == "file":
        return 400, "posting non-'file' type to /file is forbidden"

    # checks if user is authenticated
    if not helpers.authenticate(username, cookie):
        return 401, "unauthorized"

    # check chatroom permission
    if not helpers.check_access(username , chatroom_id):
        return 401, "chatroom doesnt exist or user doesnt have access to view it"

    filename = uuid.uuid1()

    # try and save the file that the user sent
    if not helpers.save_file(data, chatroom_id, mime_type, extension, filename):
        return 500, "internal server error while saving your file"


    # save a reference to the file in the chatroom database
    response = helpers.save_in_db(

            time=time.time(),
            username=username,
            chatroom_id=chatroom_id,
            message_type=message_type,
            filename=filename,
            mime_type=mime_type,
            extension=extension

            )


    return 200, response


def download_file(json_data):
    return 200, 'filename'
