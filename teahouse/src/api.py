""" Functions almost directly exposed to users """

import time

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
    channel_obj, status = database.init_chat(chatroomID, chatroom_name)
    if status != 200:
        log.error(create_chatroom, f"Failed to create chatroom database.\n Traceback: {res}")

        # remove the chatroom folders
        filesystem.remove_chatroom(chatroomID)
        return channel_obj, status


    # channel_obj is structured like:
    # {
    #         chatroom_name: "default",
    #         channelID: "id"
    #         }
    channelID = channel_obj['channelID']


    # add user to chatroom
    userID, status = users.add_user(username, password, chatroomID)
    if status != 200:
        return userID, status


    # add initial message
    messageID, status = database.write_message(chatroomID, channelID, userID, None, None, "system", f"Welcome {username}!")
    if status != 200:
        return messageID, status


    toret = {
            "chatroom_name": chatroom_name,
            "chatroomID": chatroomID,
            "channels": [
                {
                    "channel_name": 'default',
                    "channelID": channelID,
                    "public": True,
                    "permissions": { "r": True, "w": True, "x": True }
                    }
                ],
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
    if status != 200: return res, status


    # get all channels for the client
    channels, status = database.get_readable_channels(chatroomID, userID)
    if status != 200: return channels, status


    # These need to be returned for set_cookie.
    toret = {
            "chatroomID": chatroomID,
            "userID": userID,
            "channels": channels
            }
    return toret, 200




def get_channels(chatroomID: str, json_data: dict):
    """ Get all chatrooms, and their permissions """

    # get arguments
    # Dont have to check userID as its needed for authentication,
    #   and it will have already been checked
    userID = json_data.get('userID')


    # get all channels that the user can read
    channels, status = database.get_readable_channels(chatroomID, userID)
    if status != 200: return channels, status


    # Get permissions for channels.
    # This is not strictly needed as all channels
    #   in this list can be read, but I think it
    #   provides the user with some useful information.
    channels_list_with_perms = []
    for channel in channels:
        channel, status = database.get_channel_permissions(chatroomID, channel['channelID'], userID)
        if status != 200: return channels, status

        channels_list_with_perms.append(channel)


    return channels_list_with_perms, 200

def create_channel(chatroomID: str, json_data: dict):
    """ Create a channel """

    # get arguments
    # Dont have to check userID as its needed for authentication,
    #   and it will have already been checked
    userID = json_data.get('userID')

    channel_name = json_data.get('channel_name')
    is_public = True

    # check some data
    if not channel_name:
        return "You must specify a channel_name!", 400
    if type(is_public) != bool:
        return "Value for 'public_channel' has to be boolian!", 400


    # NOTE currently only the chatroom constructor can add channels,
    #   we should probably change this, and add modifyable classes like discord has.
    if userID != '0':
        return "You do not have permission to perform this action.\
                    Currently only the chatroom constructor can modify settings.\
                    (this will probably change in the future)", 403


    # save channel in db
    channelID, status = database.add_channel(chatroomID, channel_name, is_public)
    if status != 200:
        return channelID, status


    return {
            "channelID": channelID,
            "channel_name": channel_name,
            "public": is_public,
            "permissions": { "r": True, "w": True, "x": True }
            }, 200




def send_message(chatroomID: str, json_data: dict):
    """ Save message sent from user """

    replyID   = json_data.get('replyID')
    mtype     = 'text'

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
                                                # If uid is 0 then you dont need to check it.
    for i, a in enumerate([replyID, channelID, (userID if userID != '0' else None)]):
        if a != None and not security.is_uuid(a):
            return f"Value for {values[i]} is not a valid ID!", 400


    # Make sure message is of allowed type
    if mtype != 'text':
        return "Only messages with type 'text' are permitted for this method!", 400


    # users should not be able to send empty messages
    if len(mtext) < 1:
        return "Cannot send empty message", 400


    # Check if channel exists and that the user has access to it
    channel_obj, status = database.get_channel_permissions(chatroomID, channelID, userID)
    if status != 200:
        return channel_obj, status


    # NOTE maybe someone writing should have read permission as well
    if channel_obj['permissions']['w'] == False:
        return "You do not have permission to write in this channel!", 403


    return database.write_message(chatroomID, channelID, userID, replyID, keyID, 'text', mtext)

def get_messages(chatroomID: str, json_data: dict):
    """ Get the last x messages since <time> """

    # get data
    count = json_data.get('count')
    userID = json_data.get('userID')
    timebefore = json_data.get('time')
    channelID = json_data.get('channelID')


    # set default values
    count = (count if count != None else 10)
    timebefore = (timebefore if timebefore != None else time.time())


    # validate if channelID is of a proper UUID format
    if channelID != None and not security.is_uuid(channelID):
        return "ChannelID is not a valid UUID", 400


    # make sure variables have the right type
    try:
        # IMPORTANT count has to be checked because it can lead to sqli
        count = int(count)
    except Exception as e:
        return f"Could not convert variable 'count' to an integer: {e}", 400

    try:
        timebefore = float(timebefore)
    except Exception as e:
        return f"Could not convert variable 'timebefore' to float: {e}", 400


    # if a user specified a channel to get from, then add that into a 1 element list
    if channelID != None and security.is_uuid(channelID):
        channels = [{
                "channelID": channelID
                }]


    # if user did not specify any channel then get a list of readable channels
    else:
        channels, status = database.get_readable_channels(chatroomID, userID)
        if status != 200: return channels, status


    # get only the id of each channel
    channel_ids = []
    for i in channels:
        channel_ids.append(i['channelID'])


    return database.get_messages(chatroomID, count, timebefore, channel_ids)



def create_invite(chatroomID: str, json_data: dict):
    """ Create an invite for a chatroom """

    uses       = json_data.get('uses')
    userID     = json_data.get('userID')
    bestbefore = json_data.get('bestbefore')

    # placeholder for when classes work
    classID    = None



    # if not set assing default variable, if set then try convert values to their correct types
    try:
        uses = (int(uses) if uses != None else 1)
    except Exception as e:
        return f"Could not convert variable 'uses' to integer: {e}", 400

    try:
        bestbefore = (float(bestbefore) if bestbefore != None else time.time() + 60*60*24*7) 
    except Exception as e:
        return f"Could not convert variable 'bestbefore' to float: {e}", 400


    # NOTE this should be updated when classes and chatroom settings work
    if userID != '0':
        return "Permission denied: you do not have permission to create an invite", 403


    # save invite
    inviteID, status = database.write_invite(chatroomID, userID, classID, bestbefore, uses)
    if status != 200: return inviteID, status


    # create a sharable invite code
    invite_code = f"teahaz:{chatroomID}/{inviteID}"


    return {
            "invite": invite_code,
            "uses": uses,
            "bestbefore": bestbefore,
            "inviteID": inviteID
            }, 200



def get_users(chatroomID: str, json_data: dict):
    """ Get all users of a chatroom """

    # NOTE maybe later add option to filter by channel, where it only gets users that have permission to view a channel.
    # ofc that would only be available to users that can already view that channel.

    # NOTE this only gets a single user rn, but as there are no invites yet its not a huge problem.
    user_data, status = database.fetch_user(chatroomID, '0')
    return [user_data], 200




