""" Functions almost directly exposed to users """

import users_th as users
import dbhandler as database
import security_th as security
import filesystem_th as filesystem


# setup logging
from logging_th import logger
global log
log = logger()


def create_chatroom(json_data):
    """ Create a chatroom """

    # get arguments
    username      = json_data.get('username')
    password      = json_data.get('password')
    chatroom_name = json_data.get('chatroom_name')


    # generate ID for chatroom
    chatroomID    = security.gen_uuid()


    # Make sure all arguments are given
    required = ['username', 'password', 'chatroom_name']
    for i, a in enumerate([username, password, chatroom_name]):
        if a == None:
            return f"No value supplied for required field: {required[i]}", 400


    # Create folders needed for chatroom
    res, status = filesystem.create_chatroom_folders(chatroomID)
    if status != 200:
        log.error(create_chatroom, "Failed to create chatroom folders!")
        return res, 500


    # Create and set up main.db in the chatroom folder
    channelID, status = database.init_chat(chatroomID, chatroom_name)
    if status != 200:
        log.error(create_chatroom, f"Failed to create chatroom database.\n Traceback: {res}")

        # remove the chatroom folders
        filesystem.remove_chatroom(chatroomID)
        return channelID, status


    # add user to chatroom
    userID, status = users.add_user(username, password, chatroomID)
    if status != 200:
        return userID, status


    # add initial message
    messageID, status = database.write_message(chatroomID, channelID, userID, None, None, "system", f"Wellcome {username}!")
    if status != 200:
        return messageID, status


    toret = {
            "chatroom_name": chatroom_name,
            "chatroomID": chatroomID,
            "channelID": channelID,
            "userID": userID
            }
    return toret, 200


def login(chatroomID: str, json_data: dict):
    """ Login to chatroom """

    # get arguments
    userID   = json_data.get('userID')
    password = json_data.get('password')

    # Make sure all arguments are given
    required = ['userID', 'password']
    for i, a in enumerate([userID, password]):
        if a == None:
            return f"No value supplied for required field: {required[i]}", 400

    # authenticate user
    res, status = users.auth_user(chatroomID, userID, password)
    if status != 200:
        return res, status

    # These need to be returned for set_cookie.
    toret = {
            "chatroomID": chatroomID,
            "userID": userID
            }
    return toret, 200


def send_message(chatroomID: str, json_data: dict):
    """ Save message sent from user """

    replyID   = json_data.get('replyID')
    mtype     = json_data.get('mtype')

    channelID = json_data.get('channelID')
    userID    = json_data.get('userID')

    keyID     = None
    mtext     = json_data.get('data')



    # Make sure all arguments are given
    required = ["mtype", "channelID", "userID", "data"]
    for i, a in enumerate([mtype, channelID, userID, mtext]):
        if a == None:
            return f"No value supplied for required field: {required[i]}.", 400


    # Validate user input
    values = ["replyID", "channelID" ,"userID"] # , "keyID" ]
    for i, a in enumerate([replyID, channelID, userID]):
        if not security.is_uuid(a):
            return f"Value for {values[i]} is not a valid ID!", 400


    # Make sure message is of allowed type
    if mtext != 'text':
        return "Only messages with type 'text' are permitted for this method!"


    # Check if channel exists and that the user has access to it
    # NOTE kinda need to finish this
    return database.fetch_channel(chatroomID, channelID, userID)
