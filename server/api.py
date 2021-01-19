# this file handles everything connected to the message databeases
# modules
import uuid
import time
import json
import base64
from os.path import isfile as checkfile

# local
import dbhandler
import security_l as security
import filesystem_l as filehander
from logging_l import logger as log



def message_send(json_data):
    # get the data needed for this function
    try:
        username = json_data['username']
        chatroom_id = json_data['chatroom']
        message_type = json_data['type']
        message = json_data['message']
    except:
        log(level='warning', msg='[server/api/message_get/0] one or more of the required arguments are not supplied')
        return 'one or more of the required arguments are not supplied, needed=[chatroom_id, type, message]', 400


    # check message type
    if not message_type == "text":
        return "posting non-'text' type to /message is forbidden", 400

    # check chatroom permission
    if not dbhandler.check_access(username , chatroom_id):
        return "chatroom doesnt exist or user doesnt have access to view it", 401


    # store message that got sent
    if not dbhandler.save_in_db(
            time=time.time(),
            username=username,
            chatroom_id = chatroom_id,
            message_type='text',
            message=message
            ):
        return "server failed to save mesage", 500

    return "OK", 200


def message_get(headers):
    try:
        username = headers['username']
        chatroom_id = headers['chatroom']
        last_time = headers['time']
    except:
        log(level='warning', msg='[server/api/message_get/0] one or more of the required arguments are not supplied')
        return 'one or more of the required arguments are not supplied', 400


    try:## pls make sure to error check this
        last_time = float(last_time)
    except:
        log(level='error', msg='[server/api/message_get/1] value for last get time, could not be converted to a floating point number')
        return 'value for time is not a number', 400

    # check chatroom permission
    if not dbhandler.check_access(username , chatroom_id):
        log(level='error', msg=f'[server/api/message_get/2] chatroom: {chatroom_id} doesnt exist or user doesnt have access to view it')
        return "chatroom doesnt exist or user doesnt have access to view it", 401

    return_data = dbhandler.get_messages(last_time=last_time, chatroom_id=chatroom_id)

    if return_data == False:
        log(level='error', msg=f'[server/api/message_get/3] server error while getting messages')
        return "server error while getting messages", 500


    #print(d(username), d(cookie), d(last_time), d(convId))
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
        return "chatroom doesnt exist or user doesnt have access to view it", 401

    filename = str(uuid.uuid1())

    # try and save the file that the user sent
    if not filehander.save_file(data, chatroom_id, extension, filename):
        log(level='error', msg=f'[server/api/upload_file/3] failed to save file: {filename}')
        return "internal server error while saving your file", 500


    # save a reference to the file in the chatroom database
    return_data = dbhandler.save_in_db(
            time=time.time(),
            username=username,
            chatroom_id=chatroom_id,
            message_type=message_type,
            filename=filename,
            extension=extension
            )

    if return_data == False:
        log(level='error', msg=f'[server/api/upload_file/3] failed to save file: {filename}, in database')
        return "internal server error while indexing your file", 500


    return return_data, 200


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
        return "chatroom doesnt exist or user doesnt have access to view it", 401


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
        return "file requested by client does not exist", 401

    data = filehander.read_file(chatroom_id, filename)
    # read failed
    if data == False:
        log(level='error', msg=f'[server/api/download_file/4] error while reading file: {filename}')
        return "internal server error while reading user requested file", 401


    return data, 200


