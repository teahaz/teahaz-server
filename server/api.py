import uuid
import time
import json
import base64
from os.path import isfile as os_isfile

import dbhandler
import security_th as security
import filesystem_th as filehander
from logging_th import logger as log


def message_get(headers):
    last_time = headers.get('time')
    username = headers.get('username')
    chatroom_id = headers.get('chatroom')


    # make sure the client sent everything
    if not last_time or not username or not chatroom_id:
        return 'one or more of the required arguments are not supplied', 400


    # time needs to be converted to a number
    try:
        last_time = float(last_time)


    # please supply a valid time
    except:
        return 'value for time is not a number', 400


    # check the users permission to get messages from the chatroom
    response, status_code = dbhandler.check_access(username , chatroom_id)
    if status_code != 200:
        return response, status_code


    # get messages since last_time
    return_data, status_code = dbhandler.get_messages_db(last_time=last_time, chatroom_id=chatroom_id)


    # if gettting messages failed
    if status_code != 200:
        log(level='error', msg=f'[server/api/message_get/3] server error while getting messages\n Traceback  {return_data}')
        return return_data, status_code


    # all is well
    return return_data, 200


def message_send(json_data):
    chatroom_id = json_data.get('chatroom')
    username = json_data.get('username')
    message_type = json_data.get('type')
    message = json_data.get('message')
    messageId = str(uuid.uuid1())


    # make sure all of the needed data is present and is not 'None'
    if not username or not message or not message_type or not chatroom_id:
        return 'one or more of the required arguments are not supplied, needed=[chatroom_id, type, message]', 400


    # check message type
    if message_type != "text":
        return "posting non-'text' type to /message is forbidden", 405


    # check chatroom permission
    ## because username and cookie are checked together, its alright to only check the username here, and in the rest of the app
    response, status_code = dbhandler.check_access(username , chatroom_id)
    if status_code != 200:
        return response, status_code


    # store message that got sent
    #NOTE
    response , status_code = dbhandler.save_in_db(
                                time         = time.time(),
                                messageId    = messageId,
                                username     = username,
                                chatroom_id  = chatroom_id,
                                message_type = 'text',
                                message      = message
                                )


    # make sure saving worked without any errors
    if status_code != 200:
        return response, status_code

    # all is well
    return "OK", 200


def download_file(headers):
    username     = headers.get('username')
    filename     = headers.get('filename')
    chatroom_id  = headers.get('chatroom')


    # make sure client sent all data
    if not username or not filename or not chatroom_id:
        return 'one or more of the required arguments are not supplied', 400


    # check if chatroom_id is valid, this is important as its used as part of a path and in sql
    chatroom_id, status_code = security.sanitize_chatroomId(chatroom_id)
    if status_code != 200:
        return chatroom_id, status_code


    # check chatroom permission, and existance
    response, status_code = dbhandler.check_access(username , chatroom_id)
    if status_code != 200:
        return response, status_code


    # gotta sanitize shit
    filename, status_code = security.sanitize_filename(filename)
    if status_code != 200:
        return filename, status_code


    # check for the files existance. os_isfile is an alias to os.path.isfile, i dont really want to import os to minimize security issues
    if not os_isfile(f'storage/{chatroom_id}/uploads/{filename}'):
        return "file requested by client does not exist", 404


    # read file requested by user
    data, status_code = filehander.read_file(chatroom_id, filename)
    if status_code != 200:
        log(level='error', msg=f'[server/api/download_file/0] error while reading file: {filename}')
        return data, status_code


    # all is well
    return data, 200


def upload_file(json_data):
    username      = json_data.get('username')
    chatroom_id   = json_data.get('chatroom')
    message_type  = json_data.get('type')
    data          = json_data.get('data')
    extension     = json_data.get('extension')
    messageId     = uuid.uuid1()



    # make sure client sent all needed data
    if not username or not chatroom_id or not message_type or not data or not extension:
        return 'one or more of the required arguments are not supplied', 400


    # message type has to be file
    if not message_type == "file":
        return "posting non-'file' type to /file is forbidden", 400


    # check chatroom permission, and existance
    response, status_code = dbhandler.check_access(username , chatroom_id)
    if status_code != 200:
        return "chatroom doesnt exist or user doesnt have access to view it", 404


    # generate filename
    filename = str(uuid.uuid1())


    # save file that user sent
    response, status_code = filehander.save_file(data, chatroom_id, extension, filename)
    if status_code != 200:
        log(level='error', msg=f'[server/api/upload_file/0] failed to save file: {filename}')
        return response, status_code


    # save a reference to the file in the chatroom database
    response, status_code = dbhandler.save_in_db(
            time          = time.time(),
            messageId     = messageId,
            username      = username,
            chatroom_id   = chatroom_id,
            message_type  = message_type,
            filename      = filename,
            extension     = extension
            )


    # failed to save reference to file
    if status_code != 200:
        log(level='warning', msg=f'[server/api/upload_file/1] failed to save file: {filename}, in database \n attempting to remove')

        # delete file because it could not be indexed
        _response, status_code = filehander.remove_file(chatroom_id, filename)
        if status_code != 200:
            log(level='error', msg=f'[server/api/upload_file/2] failed to delete corrupt file: {filename}')

        # return error
        return response, status_code


    # all is well
    return response, 200


def create_chatroom(json_data):
    username      = json_data.get('username')
    chatroomId    = str(uuid.uuid1())
    chatroom_name = json_data.get('chatroom_name')


    # make sure client sent all needed data
    if not username or not chatroomId or not chatroom_name:
        return 'one or more of the required arguments are not supplied', 400


    # create folders needed for chatroom
    response, status_code = filehander.create_chatroom_folders(chatroomId)
    if status_code != 200:
        log(level='error', msg=f'[server/api/create_chatroom/0] could not create chatroom\n Traceback: {response}')
        return "internal server error", 500


    # create chatroom.db inside chatroom the chatrom folder
    response, status_code = dbhandler.init_chat(chatroomId)
    if status_code != 200:
        log(level='error', msg=f'[server/api/create_chatroom/1] could not create chatroom database\n Traceback: {response}')
        return "internal database error", 500


    # make entry in main.db
    response, status_code = dbhandler.save_chatroom(chatroomId, chatroom_name)
    if status_code != 200:
        log(level='error', msg=f'[server/api/create_chatroom/2] could not create chatroom entry in main.db\n Traceback: {response}')
        return "internal database error", 500


    response, status_code = dbhandler.user_save_chatroom(username, chatroomId)
    if status_code != 200:
        log(level='error', msg=f'[server/api/create_chatroom/3] could not save chatroom for user in main.db\n Traceback: {response}')
        return "internal database errror", 500


    return chatroomId, 200


def get_chatrooms(headers):
    username = headers.get('username')


    # make sure we got all needed data
    if not username:
        return "username not supplied", 400


    # get a list of chatroom IDs that the user has access to
    response, status_code = dbhandler.user_get_chatrooms(username)

    print('response: ',response , type(response))
    print('status_code: ',status_code , type(status_code))
    # if error
    if status_code != 200:
        log(level='error', msg=f'[server/api/get_chatrooms/3] could not get chatroom data from main.db')
        return response, status_code


    # if not error
    else:
        # if there are non then respond with 204
        if len(response) == 0:
            return "", 204

        # create json with chatname and chat ID in it
        print('response: ',response , type(response))
        resp_list = []
        for chatroomId in response:
            print('chatroomId: ',chatroomId , type(chatroomId))


            # get name corresponding to  chatroomId
            chatname, status_code = dbhandler.get_chatname(chatroomId)
            if status_code != 200:
                return chatname, status_code


            chat_obj = {
                    'name': chatname,
                    'chatroomId': chatroomId
                    }


            resp_list.append(chat_obj)
        response = resp_list

    # all is well
    return response, status_code




