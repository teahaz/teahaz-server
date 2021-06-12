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
    res, status = database.init_chat(chatroomID, chatroom_name)
    if status != 200:
        log.error(create_chatroom, "Failed to create chatroom database.\n Traceback: {res}")

        # remove the chatroom folders
        filesystem.remove_chatroom(chatroomID)
        return res, status


    # add user to chatroom

