import uuid
import time
import json
import base64
from os.path import isfile as os_isfile

import dbhandler
import security_th as security
import filesystem_th as filehander
import users_th as users
from logging_th import logger as log 





def create_chatroom(json_data):
    username      = json_data.get('username')
    email         = json_data.get('email')
    nickname      = json_data.get('nickname')
    password      = json_data.get('password')
    chatroom_name = json_data.get('chatroom_name')
    chatroomId    = str(uuid.uuid1())


    # make sure client sent all needed data
    if not username or not email or not nickname or not password or not chatroom_name:
        return '[api/create_chatroom/0] || One or more of the required arguments are not supplied. required = [username, email, nickname, password, chatroom_name]', 400



    # create folders needed for chatroom
    response, status_code = filehander.create_chatroom_folders(chatroomId)
    if status_code != 200:
        log(level='error', msg=f'[api/create_chatroom/2] || could not create chatroom')
        return response, 500



    # create chatroom.db inside chatroom the chatrom folder
    response, status_code = dbhandler.init_chat(chatroomId, chatroom_name)
    if status_code != 200:
        log(level='error', msg=f'[api/create_chatroom/3] || could not create chatroom database\n Traceback: {response}')

        # remove chatroom
        filehander.remove_chatroom(chatroomId)

        return response, status_code



    response, status_code = users.add_user(username, email, nickname, password, chatroomId)
    if status_code != 200:
        log(level='error', msg="[api/create_chatroom/4] || Failed to add chatroom admin")

        # remove chatroom
        filehander.remove_chatroom(chatroomId)

        return response, status_code


    response, status_code = dbhandler.check_settings(chatroomId, "chatroom_name")
    if status_code != 200:
        return response, status_code



    # format chat object
    try:
        chat_obj = {
                "name": response,
                "chatroom": chatroomId
                }
    except Exception as e:
        log(level='error', msg=f"[api/create_chatroom/5] || Formattng chat_obj failed: {e}")
        return "[api/create_chatroom/5] || Internal server errror while formatting chat object", 500


    # run set_cookie for autolong, and chatobj for returning at the end
    return chat_obj, 200



def create_invite(json_data, chatroomId):
    username   = json_data.get('username')
    expr_time  = json_data.get('expr_time')
    uses       = json_data.get('uses')
    inviteId   = str(uuid.uuid1())


    # make sure we got all the data
    if not username or not chatroomId or not uses or not expr_time:
        return "[api/create_invite/0] || One or more of the required arguments were not supplied. Required=[username, chatroom, expr_time, uses]", 400


    # make sure the format is good on time and uses
    try:
        expr_time = float(expr_time)
        uses = int(uses)


    # no
    except:
        return "[api/create_invite/1] || Invalid format: expr_time has to be type: FLOAT AND uses has to by type: INT", 400


    # invites can only be created if you are admin
    has_permission, status_code = dbhandler.check_perms(username, chatroomId, permission="admin")
    if status_code != 200:
        return has_permission, status_code


    if has_permission != True:
        return "[api/create_invite/2] || Permission denied: your user does not have permission to perform this action", 403


    # save this invite in the database
    response, status_code = dbhandler.save_invite(chatroomId, inviteId, expr_time, uses)
    if status_code != 200:
        return response, status_code


    # ok
    return inviteId, 200

















#def get_chatrooms(headers):
#    username = headers.get('username')
#
#
#    # make sure we got all needed data
#    if not username:
#        return "username not supplied", 400
#
#
#    # get a list of chatroom IDs that the user has access to
#    response, status_code = dbhandler.user_get_chatrooms(username)
#
#    # if error
#    if status_code != 200:
#        log(level='error', msg=f'[server/api/get_chatrooms/3] could not get chatroom data from main.db')
#        return response, status_code
#
#
#    # if not error
#    else:
#        # if there are non then respond with 204
#        if len(response) == 0:
#            return "", 204
#
#        # create json with chatname and chat ID in it
#        resp_list = []
#        for chatroomId in response:
#
#            # get name corresponding to  chatroomId
#            chatname, status_code = dbhandler.get_chatname(chatroomId)
#            if status_code != 200:
#                return chatname, status_code
#
#
#            chat_obj = {
#                    'name': chatname,
#                    'chatroom': chatroomId
#                    }
#
#
#            resp_list.append(chat_obj)
#        response = resp_list
#
#    # all is well
#    return response, status_code


#
#def message_get(headers):
#    last_time = headers.get('time')
#    username = headers.get('username')
#    chatroom_id = headers.get('chatroom')
#
#
#    # make sure the client sent everything
#    if not last_time or not username or not chatroom_id:
#        return 'one or more of the required arguments are not supplied', 400
#
#
#    # time needs to be converted to a number
#    try:
#        last_time = float(last_time)
#
#
#    # please supply a valid time
#    except:
#        return 'value for time is not a number', 400
#
#
#    # get messages since last_time
#    return_data, status_code = dbhandler.get_messages_db(chatroom_id, last_time=last_time, )
#
#
#    # if gettting messages failed
#    if status_code != 200:
#        log(level='error', msg=f'[server/api/message_get/3] server error while getting messages\n Traceback  {return_data}')
#        return return_data, status_code
#
#
#    # all is well
#    return return_data, 200
#
#
#
#def message_send(json_data):
#    chatroom_id = json_data.get('chatroom')
#    username = json_data.get('username')
#    message_type = json_data.get('type')
#    message = json_data.get('message')
#    messageId = str(uuid.uuid1())
#
#
#    # make sure all of the needed data is present and is not 'None'
#    if not username or not message or not message_type or not chatroom_id:
#        return 'one or more of the required arguments are not supplied, needed=[chatroom_id, type, message]', 400
#
#
#    # check message type
#    if message_type != "text":
#        return "posting non-'text' type to /message is forbidden", 405
#
#
#    # store message that got sent
#    #NOTE
#    response , status_code = dbhandler.save_in_db(
#                                time         = time.time(),
#                                messageId    = messageId,
#                                username     = username,
#                                chatroomId  = chatroom_id,
#                                message_type = 'text',
#                                message      = message
#                                )
#
#
#    # make sure saving worked without any errors
#    if status_code != 200:
#        return response, status_code
#
#    # all is well
#    return "OK", 200
#
#
#
#def download_file(headers):
#    username     = headers.get('username')
#    filename     = headers.get('filename')
#    chatroom_id  = headers.get('chatroom')
#
#
#    # make sure client sent all data
#    if not username or not filename or not chatroom_id:
#        return 'one or more of the required arguments are not supplied', 400
#
#
#    # check if chatroom_id is valid, this is important as its used as part of a path and in sql
#    chatroom_id, status_code = security.sanitize_chatroomId(chatroom_id)
#    if status_code != 200:
#        return chatroom_id, status_code
#
#
#    # gotta sanitize shit
#    filename = security.sanitize_uuid(filename)
#    if not filename:
#        return "invalid format from filename", 400
#
#
#    # check for the files existance. os_isfile is an alias to os.path.isfile, i dont really want to import os to minimize security issues
#    if not os_isfile(f'storage/{chatroom_id}/uploads/{filename}'):
#        return "file requested by client does not exist", 404
#
#
#    # read file requested by user
#    data, status_code = filehander.read_file(chatroom_id, filename)
#    if status_code != 200:
#        log(level='error', msg=f'[server/api/download_file/0] error while reading file: {filename}')
#        return data, status_code
#
#
#    # all is well
#    return data, 200
#
#
#
#def upload_file(json_data):
#    username      = json_data.get('username')
#    chatroom_id   = json_data.get('chatroom')
#    message_type  = json_data.get('type')
#    data          = json_data.get('data')
#    extension     = json_data.get('extension')
#    messageId     = uuid.uuid1()
#
#
#
#    # make sure client sent all needed data
#    if not username or not chatroom_id or not message_type or not data or not extension:
#        return 'one or more of the required arguments are not supplied', 400
#
#
#    # message type has to be file
#    if not message_type == "file":
#        return "posting non-'file' type to /file is forbidden", 400
#
#
#
#    # generate filename
#    filename = str(uuid.uuid1())
#
#
#    # save file that user sent
#    response, status_code = filehander.save_file(data, chatroom_id, extension, filename)
#    if status_code != 200:
#        log(level='error', msg=f'[server/api/upload_file/0] failed to save file: {filename}')
#        return response, status_code
#
#
#    # save a reference to the file in the chatroom database
#    response, status_code = dbhandler.save_in_db(
#            time          = time.time(),
#            messageId     = messageId,
#            username      = username,
#            chatroomId   = chatroom_id,
#            message_type  = message_type,
#            filename      = filename,
#            extension     = extension
#            )
#
#
#    # failed to save reference to file
#    if status_code != 200:
#        log(level='warning', msg=f'[server/api/upload_file/1] failed to save file: {filename}, in database \n attempting to remove')
#
#        # delete file because it could not be indexed
#        _response, status_code = filehander.remove_file(chatroom_id, filename)
#        if status_code != 200:
#            log(level='error', msg=f'[server/api/upload_file/2] failed to delete corrupt file: {filename}')
#
#        # return error
#        return response, status_code
#
#
#    # all is well
#    return response, 200
#
#
#
#
#
