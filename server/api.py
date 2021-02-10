# this file handles everything connected to the message databeases
# modules
import uuid
import time
import json
import base64
from os.path import isfile as checkfile

# local
import dbhandler
import security_th as security
import filesystem_th as filehander
from logging_th import logger as log



def message_send(json_data):
    chatroom_id = json_data.get('chatroom')
    username = json_data.get('username')
    message_type = json_data.get('type')
    message = json_data.get('message')


    # make sure all of the needed data is present and is not 'None'
    if not username or not message or not message_type or not chatroom_id:
        log(level='warning', msg='[server/api/message_get/0] one or more of the required arguments are not supplied')
        return 'one or more of the required arguments are not supplied, needed=[chatroom_id, type, message]', 400


    # check message type
    if message_type != "text":
        log(level='warning', msg='[server/api/message_get/0] posting non-"text" type to /message is forbidden')
        return "posting non-'text' type to /message is forbidden", 405


    # check chatroom permission
    ## because username and cookie are checked together, its alright to only check the username here, and in the rest of the app
    response, status_code = dbhandler.check_access(username , chatroom_id)
    if status_code != 200:
        return response, status_code


    # store message that got sent
    #NOTE
    response , status_code = dbhandler.save_in_db(
                                time=time.time(),
                                username=username,
                                chatroom_id = chatroom_id,
                                message_type='text',
                                message=message
                                )


    # make sure saving worked without any errors
    if status_code != 200:
        return response, status_code

    # all is well
    return "OK", 200


# get messages sent since <time>
def message_get(headers):
    last_time = headers.get('time')
    username = headers.get('username')
    chatroom_id = headers.get('chatroom')


    # make sure the client sent everything
    if not last_time or not username or not chatroom_id:
        log(level='warning', msg='[server/api/message_get/0] one or more of the required arguments are not supplied')
        return 'one or more of the required arguments are not supplied', 400


    # time needs to be converted to a number
    try:
        last_time = float(last_time)


    # please supply a valid time
    except:
        log(level='error', msg='[server/api/message_get/1] value for last get time, could not be converted to a floating point number')
        return 'value for time is not a number', 400


    # check the users permission to get messages from the chatroom
    response, status_code = dbhandler.check_access(username , chatroom_id)
    if status_code != 200:
        log(level='error', msg=f'[server/api/message_get/2] chatroom: {chatroom_id} doesnt exist or user doesnt have access to view it')
        return response, status_code


    # get messages since last_time
    return_data, status_code = dbhandler.get_messages_db(last_time=last_time, chatroom_id=chatroom_id)


    # if gettting messages failed
    if status_code != 200:
        log(level='error', msg=f'[server/api/message_get/3] server error while getting messages\n Traceback  {return_data}')
        return return_data, status_code


    # all is well
    return return_data, 200


def upload_file(json_data):
    try:
        username = json_data['username']
        chatroom_id = json_data['chatroom']
        message_type = json_data['type']
        data = json_data['data']
        extension = json_data['extension']
    except:
        log(level='warning', msg='[server/api/upload_file/0] one or more of the required arguments are not supplied')
        return 'one or more of the required arguments are not supplied', 400

    # check message type
    if not message_type == "file":
        log(level='error', msg='[server/api/upload_file/1] client attempted to post message with type other then "file" to /file')
        return "posting non-'file' type to /file is forbidden", 400

    # check chatroom permission, and existance
    if not dbhandler.check_access(username , chatroom_id):
        log(level='error', msg=f'[server/api/upload_file/2] chatroom: {chatroom_id} doesnt exist or user: {username} doesnt have access to view it')
        return "chatroom doesnt exist or user doesnt have access to view it", 404

    filename = str(uuid.uuid1())

    # try and save the file that the user sent
    if not filehander.save_file(data, chatroom_id, extension, filename):
        log(level='error', msg=f'[server/api/upload_file/3] failed to save file: {filename}')
        return "internal server error while saving your file", 500


    # save a reference to the file in the chatroom database
    response, status_code = dbhandler.save_in_db(
            time=time.time(),
            username=username,
            chatroom_id=chatroom_id,
            message_type=message_type,
            filename=filename,
            extension=extension
            )

    if status_code != 200:
        log(level='error', msg=f'[server/api/upload_file/3] failed to save file: {filename}, in database')
        return response, status_code

    return response, 200


def download_file(headers):
    try:
        username = headers['username']
        chatroom_id = headers['chatroom']
        filename = headers['filename']
    except:
        log(level='warning', msg='[server/api/download_file/0] client did not supply all the needed arguments for this function [username, chatroom, filename]')
        return 'one or more of the required arguments are not supplied', 400

    # we gotta be safe
    chatroom_id = security.sanitize_chatroomId(chatroom_id)

    # check chatroom permission, and existance
    if not dbhandler.check_access(username , chatroom_id):
        log(level='warning', msg=f'[server/api/download_file/1] chatroom: {chatroom_id} doesnt exist or user: {username} doesnt have access to view it')
        return "chatroom doesnt exist or user doesnt have access to view it", 404


    # gotta sanitize shit
    filename = security.sanitize_filename(filename)
    # if sanitization of filename failed
    if filename == False:
        log(level='warning', msg=f'[server/api/download_file/2] user specified file is of invalid format [ must be 36 bytes long ]')
        return "user specified file was not of accepted format", 400


    # check for the files existance
    # checkfile is an alias to os.path.isfile
    if not checkfile(f'storage/{chatroom_id}/uploads/{filename}'):
        log(level='error', msg=f'[server/api/download_file/3] file storage/{chatroom_id}/uploads/{filename} does not exist')
        return "file requested by client does not exist", 404

    data = filehander.read_file(chatroom_id, filename)
    # read failed
    if data == False:
        log(level='error', msg=f'[server/api/download_file/4] error while reading file: {filename}')
        return "internal server error while reading user requested file", 404


    return data, 200


