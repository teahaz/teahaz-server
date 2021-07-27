"""
    A few functions that need to be called many times, often in different files.
"""

import users_th as users
import dbhandler as database
import filesystem_th as filesystem

# setup logging
from logging_th import logger
global log
log = logger()



#################################################### main ########################################
def check_default(method: str, chatroomID: str, request: object, need_login: bool):
    """
        A series of checks that need to be performed in every method

        need_login:
            option should be true or false depending on wether cookies have to be checked
    """


    # If method is get then data has to be sent in headers
    data = (request.get_json() if method != 'get' else request.headers)


    # Make sure there was anything sent to the server
    if not data: return "no data sent", 401


    # ChatroomId is only none in the create chatroom method,
    #   in which case its enough to just check the data
    if chatroomID == None:
        return "Ok", 200


    # Check if chatroom exists
    if not filesystem.chatroom_exists(chatroomID): return "Chatroom does not exist.", 404


    if need_login == True:
        if not users.check_cookie(chatroomID, request.cookies.get(chatroomID), data.get('username')):
            return "Client not logged in. (Cookie or username was invalid, or not sent)", 401


    return "OK", 200



#################################################### dbhandler ###################################
def db_format_channel(channel_info: list):
    """
        Format the list of tuples that the channels db returns into a dict

        return:
            {
                channelID: "channelID",
                channel_name: "channel_name",
                public: False
            }
    """



    # this type of operation can crash the server if I fuck something up in the table
    # I need an error message bc this seems like it would be really hard to debug otherwise
    try:
        channel_obj = {
                "channelID": channel_info[0],
                "channel_name": channel_info[1],
                "public": channel_info[2]
                }
    except Exception as e:
        log.error(db_format_channel, f"Corrupted information in channels table. {e}")
        return "Internal database error while fetching channel information", 500


    return channel_obj, 200

def db_format_message(messages: list):
    """ Formats the output of the db response of the messages table """


    try:
        messages_list = []
        for message in messages:

            message_obj = {
                    "messageID": message[0],
                    "channelID": message[1],
                    "username"   : message[2],
                    "replyID"  : message[3],
                    "keyID"    : message[4],
                    "send_time": message[5],
                    "type"     : message[6],
                    "data"     : message[7],
                    }

            messages_list.append(message_obj)

    except Exception as e:
        log.error(db_format_message, f"An error occured while formatting message: {e}.")
        return f"Internal database error wile formatting messages.", 500

    return messages_list, 200





#################################################### other ###################################
def get_chat_info(chatroomID: str, username: str) -> (dict, int):
    """ Get all information about a chatroom """

    chatroom_data = {
            "chatroomID": chatroomID
            }

    # get chatroom settings
    settings, status = database.fetch_all_settings(chatroomID)
    if status != 200: return settings, chatroomID
    chatroom_data['settings'] = settings

    # get chatroom name
    chatroom_name, status = database.check_settings(chatroomID, 'chatroom_name')
    if status != 200: return chatroom_name, chatroomID
    chatroom_data['chatroom_name'] = chatroom_name

    # get users
    users, status = database.fetch_all_users(chatroomID)
    if status != 200: return users, status
    chatroom_data['users'] = users

    # get classes
    classes, status = database.fetch_all_classes(chatroomID)
    if status != 200: return classes, status
    chatroom_data['classes'] = classes

    # get channels
    channels, status = database.fetch_all_readable_channels(chatroomID, username)
    if status != 200: return channels, status
    chatroom_data['channels'] = channels

    return chatroom_data, 200



