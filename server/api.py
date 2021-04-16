import os
import uuid
import time
import json
import base64

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
    expr_time  = json_data.get('expr-time')
    uses       = json_data.get('uses')
    inviteId   = str(uuid.uuid1())


    # make sure we got all the data
    if not username or not chatroomId or not uses or not expr_time:
        return f"[api/create_invite/0] || One or more of the required arguments were not supplied. Required=[username, expr_time, uses]. Supplied=[{username}, {uses}, {expr_time}]", 400


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


    # log the creation of an invite
    response , status_code = dbhandler.save_in_db(
                                    chatroomId   = chatroomId,
                                    time         = time.time(),
                                    messageId    = security.gen_uuid(),
                                    kId          = None,
                                    replyId      = None,
                                    username     = username,
                                    message_type = 'system',
                                    message      = '"' + str(dbhandler.get_nickname(chatroomId, security.encode(username))) + f'" created an invite!\n uses: {uses}, expiration date: ' + str((expr_time if expr_time > 0 else "never"))
                                    )


    # ok
    return inviteId, 200




def message_send(json_data, chatroomId):
    messageId    = str(uuid.uuid1())
    replyId      = json_data.get('replyId')
    message      = json_data.get('message')
    username     = json_data.get('username')
    message_type = json_data.get('type')
    kId          = json_data.get('kId')



    # make sure all of the needed data is present and is not 'None'
    if not username or not message or not message_type or not chatroomId:
        return '[api/message_send/0] || one or more of the required arguments are not supplied, needed=[username, message, type, chatroomId]', 400


    # check message type
    if message_type != "text":
        return "[api/message_send/1] || posting non-'text' type to /message is forbidden", 405


    # store message that got sent
    #NOTE
    response , status_code = dbhandler.save_in_db(
                                chatroomId   = chatroomId,
                                time         = time.time(),
                                messageId    = messageId,
                                kId          = kId,
                                replyId      = replyId,
                                username     = username,
                                message_type = 'text',
                                message      = message
                                )


    # make sure saving worked without any errors
    if status_code != 200:
        return response, status_code

    # all is well
    return "OK", 200


def message_get(headers, chatroomId):
    username = headers.get('username')
    last_time = headers.get('time')
    messageId = headers.get('messageId')


    # make sure the client sent everything
    if  not username or not chatroomId:
        return '[api/message_get/0] || one or more of the required arguments are not supplied. Required=[username] Supplied=[{username}]', 400


    # if messageId is set then just get the message with that Id
    if messageId:
        # set the function mode to single message
        mode = 'single'

        # make sure the messageId is valid
        res, status = security.check_uuid(messageId)
        if status != 200:
            return res, status

        # make sure the other is set to None
        last_time = None



    # if messageId is not set then get all messages since <last_time>
    elif last_time:
        # set the function mode to multiple messages
        mode = 'multiple'

        # time needs to be converted to a number
        try:
            last_time = float(last_time)

        # please supply a valid time
        except:
            return '[api/message_get/1] || value for time is not a number', 400


        # make sure the other is set to None
        messageId = None


    else:
        return "[api/message_get/2] || Must send either messageId or time", 400


    # get messages since last_time
    return_data, status_code = dbhandler.get_messages_db(chatroomId, last_time=last_time, messageId=messageId)


    # if gettting messages failed
    if status_code != 200:
        log(level='error', msg=f'[server/api/message_get/3] server error while getting messages\n Traceback  {return_data}')
        return return_data, status_code


    # all is well
    return return_data, 200


def message_delete(json_data, chatroomId):
    username = json_data.get('username')
    messageId = json_data.get('messageId')


    # make sure all of the needed data is present and is not 'None'
    if not messageId or not username:
        return f'[api/message_delete/0] || one or more of the required arguments are not supplied, needed=[messageId, username], Supplied=[{messageId}, {username}]', 400


    # get message by id
    response, status_code = message_get({'username': username, 'messageId': messageId}, chatroomId)
    if status_code != 200:
        return response, status_code


    # if no message with said id
    if len(response) > 0:
        response = response[0]
    else:
        return f"[api/message_delete/1] || no message with specified ID", 404


    # get sender name
    sender_name = response.get('username')
    if not sender_name:
        log(level='error', msg='[api/message_delete/2] || could not get sender name')
        return f"[api/message_delete/2] || could not get sender name", 500


    # get admin status of user
    admin, status = dbhandler.check_perms(username, chatroomId, 'admin')
    if status != 200:
        log(level='error', msg='[api/message_delete/3] || could not get chatroom permissions')
        return f"[api/message_delete/3] || could not get chatroom permissions", 500


    # if not (user sent the message or he is admin)
    if not (username == sender_name or admin == True):
        return f"[api/message_delete/4] || could not delete message: Permission denied", 403


    response, status_code = dbhandler.delete_message(messageId, chatroomId)
    if status_code != 200:
        return response, status_code


    # save the delete action in the man database
    response , status_code = dbhandler.save_in_db(
                                chatroomId   = chatroomId,
                                time         = time.time(),
                                messageId    = security.gen_uuid(),
                                kId          = None,
                                replyId      = None,
                                username     = username,
                                message_type = 'delete',
                                message      = messageId
                                )

    return response, status_code




def upload_file(json_data, chatroomId):
    username      = json_data.get('username')
    filename      = json_data.get('filename')
    fileId        = json_data.get('fileId')
    message_type  = json_data.get('type')
    last          = json_data.get('last')
    data          = json_data.get('data')
    kId           = json_data.get('kId')

    # if there is no fileID then this is the first chunk of the file upload. In this case we assign a new fileid
    if not fileId: fileId = str(security.gen_uuid())


    # make sure client sent all needed data
    if not username or not message_type or not data or not filename:
        return f'[api/upload_file/0] || one or more of the required arguments are not supplied. Required=[username, type, data, filename]  Supplied=[{username}, {message_type}, (type(data)){type(data)}(len(data)){len(data)}, {filename})]', 400



    # message type has to be file
    if not message_type == "file":
        return "[api/upload_file/1] || posting non-'file' type to /file is forbidden", 400



    # NOTE: this should be a global setting
    max_chunk_size = 1048576 # one megabyte


    # make sure chunk is not larger than the maximum allowed size
    if len(data) > max_chunk_size:
        return f'[api/upload_file/2] || data field exeeded the maximum chunk-size permitted by the server. Maximum={max_chunk_size}', 400



    # make sure last is bool
    try: last = bool(last)
    except: return f"[api/upload_file/2] || 'last' variable must be of type 'bool'."


    # save file that user sent
    current_section, status_code = filehander.save_file_chunk(chatroomId, username, fileId, data, last)
    if status_code != 200:
        log(level='error', msg=f'[api/upload_file/2] failed to save file: {fileId}')
        return current_section, status_code




    # if the file is small or its the last part: save a reference to the file in the chatroom database
    if last == True:
        response, status_code = dbhandler.save_in_db(
                chatroomId    = chatroomId,
                time          = time.time(),
                messageId     = fileId,
                kId           = kId,
                username      = username,
                message_type  = 'file',
                fileId        = fileId,
                filename      = filename,
                filesize      = current_section + 1
                )


        # failed to save reference to file
        if status_code != 200:
            log(level='warning', msg=f'[api/upload_file/3] || failed to save file: {fileId}, in database \n attempting to remove')

            # delete file because it could not be indexed
            _response, status_code = filehander.remove_file(chatroomId, fileId)
            if status_code != 200:
                log(level='error', msg=f'[api/upload_file/4] || failed to delete corrupt file: {fileId}')

            # return error
            return response, status_code


    # all is well
    return {"fileId": fileId, "filesize": current_section+1}, 200


def download_file(headers, chatroomId):
    username     = headers.get('username')
    section      = headers.get('section')
    fileId       = headers.get('fileId')


    # make sure client sent all data
    if not username or not fileId  or not section:
        return '[api/download_file/0] || one or more of the required arguments are not supplied. Required = [username, filename, section]. Supplied=[{username}, {filename}, {section}]', 400


    # make sure section is int
    try:
        section = int(section)
    except Exception as e:
        return f'[api/download_file/1] || invalid data sent for section filed. Type has to be INT. Traceback: {e}'



    # sanitization is healthy
    response, status_code = security.check_uuid(fileId)
    if status_code != 200:
        return response, status_code



    # check for the files existance. os_isfile is an alias to os.path.isfile, i dont really want to import os to minimize security issues
    if not os.path.isdir(f'storage/chatrooms/{chatroomId}/uploads/{fileId}'):
        return "[api/download_file/2] || The requested file doesnt exist", 404



    # read file requested by user
    data, status_code = filehander.read_file_chunk(chatroomId, fileId, section)
    if status_code != 200:
        log(level='error', msg=f'[server/api/download_file/3] error while reading file: {fileId}')
        return data, status_code



    # all is well
    return {"data": data}, 200

































