""" Functions almost directly exposed to users """

import time

import users_th as users
import dbhandler as database
import security_th as security
import global_helpers as helpers
import filesystem_th as filesystem


# setup logging
from logging_th import logger
global log
log = logger()





def create_chatroom(json_data):
    """ Create a chatroom """

    # get arguments
    username      = json_data.get('username')
    nickname      = json_data.get('username')
    password      = json_data.get('password')
    chatroom_name = json_data.get('chatroom_name')


    # The nickname argument is optional and if not set it will be the same as username
    nickname      = (nickname if nickname != None else username)


    # generate ID for chatroom
    chatroomID    = security.gen_uuid()


    # Make sure all arguments are given
    required = ['username', 'password', 'chatroom_name']
    for i, a in enumerate([username, password, chatroom_name]):
        if a == None or len(a) < 1:
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
    username, status = users.add_user(chatroomID, username, nickname, password)
    if status != 200: return username, status


    # add initial message
    messageID, status = database.write_message(chatroomID, channelID, username, None, None, "system", f"Welcome {nickname}!")
    if status != 200: return messageID, status

    # return information about the created chatroom
    return helpers.get_chat_info(chatroomID, username)

def login(chatroomID: str, json_data: dict):
    """ Login to chatroom """

    # get arguments
    username   = json_data.get('username')
    password = json_data.get('password')

    # Make sure all arguments are given
    required = ['username', 'password']
    for i, a in enumerate([username, password]):
        if a == None or len(a) < 1:
            return f"No value supplied for required field: {required[i]}", 400

    # authenticate user
    res, status = users.auth_user(chatroomID, username, password)
    if status != 200: return res, status


    # get all channels for the client
    channels, status = database.get_readable_channels(chatroomID, username)
    if status != 200: return channels, status


    # These need to be returned for set_cookie.
    toret = {
            "chatroomID": chatroomID,
            "username": username,
            "channels": channels
            }
    return toret, 200




def get_channels(chatroomID: str, json_data: dict):
    """ Get all chatrooms, and their permissions """

    # NOTE replace with global_helpers.get_chat_info


    # get arguments
    # Dont have to check username as its needed for authentication,
    #   and it will have already been checked
    username = json_data.get('username')


    # get all channels that the user can read
    channels, status = database.get_readable_channels(chatroomID, username)
    if status != 200: return channels, status


    # Get permissions for channels.
    # This is not strictly needed as all channels
    #   in this list can be read, but I think it
    #   provides the user with some useful information.
    channels_list_with_perms = []
    for channel in channels:
        channel, status = database.get_channel_permissions(chatroomID, channel['channelID'], username)
        if status != 200: return channels, status

        channels_list_with_perms.append(channel)


    return channels_list_with_perms, 200

def create_channel(chatroomID: str, json_data: dict):
    """ Create a channel """

    # get arguments
    # Dont have to check username as its needed for authentication,
    #   and it will have already been checked
    username = json_data.get('username')

    channel_name = json_data.get('channel_name')
    is_public = True

    # check some data
    if not channel_name:
        return "You must specify a channel_name!", 400
    if type(is_public) != bool:
        return "Value for 'public_channel' has to be boolian!", 400


    constructor, status = database.get_constructor(chatroomID)
    if status != 200: return constructor, status

    if username != constructor:
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
    username    = json_data.get('username')

    keyID     = None
    mtext     = json_data.get('data')



    # Make sure all arguments are given
    required = ["mtype", "channelID", "username", "data"]
    for i, a in enumerate([mtype, channelID, username, mtext]):
        if a == None:
            return f"No value supplied for required field: {required[i]}.", 400


    # Validate user input
    values = ["replyID", "channelID"] # , "keyID" ]
                                                # If uid is 0 then you dont need to check it.
    for i, a in enumerate([replyID, channelID]):
        if a != None and not security.is_uuid(a):
            return f"Value for {values[i]} is not a valid ID!", 400


    # Make sure message is of allowed type
    if mtype != 'text':
        return "Only messages with type 'text' are permitted for this method!", 400


    # users should not be able to send empty messages
    if len(mtext) < 1:
        return "Cannot send empty message", 400


    # Check if channel exists and that the user has access to it
    channel_obj, status = database.get_channel_permissions(chatroomID, channelID, username)
    if status != 200:
        return channel_obj, status


    # NOTE maybe someone writing should have read permission as well
    if channel_obj['permissions']['w'] == False:
        return "You do not have permission to write in this channel!", 403


    return database.write_message(chatroomID, channelID, username, replyID, keyID, 'text', mtext)

def get_messages(chatroomID: str, json_data: dict):
    """ Get the last x messages since <time> """

    # needed/optional data:
    # Im adding this comment because most other methods
    #   have all the information at the top, but that
    #   doesnt make as much sense here.

    # data:
        # username
        # get-method
        # channelID (optional)
        # count (optional)
        # time (optional)

    username = json_data.get('username')


    # If channelID is set then get messages from just that one channel,
    #  else get from all readable channels.
    channelID = json_data.get('channelID')

    # validate if channelID is of a proper UUID format
    if channelID != None and not security.is_uuid(channelID):
        return "ChannelID is not a valid UUID", 400

    # ChannelID is set, get list of 1 element
    if channelID != None and security.is_uuid(channelID):
        channels = [{ "channelID": channelID }]

    # ChannelID is not set, get all readable
    else:
        channels, status = database.get_readable_channels(chatroomID, username)
        if status != 200: return channels, status

    # Get a list of **only** the channelIDs of needed channels.
    channel_ids = []
    for i in channels:
        channel_ids.append(i['channelID'])




    # Get method specifies how you want to get information from the server.
    #   Options for this variable are:
    #       - since  || 0
    #        get all messages since <time>
    #       - count  || 1
    #        Get <count> number of messages.
    #        This method also supports the time argument to specify a starting time.
    get_method = json_data.get('get-method')


    if get_method in ['since', 0]:
        # get since <time>

        timesince = json_data.get('time')

        # make sure variables have the right type
        try:
            timesince = float(timesince)
        except Exception as e:
            return f"Could not convert variable 'time' to float: {e}", 400

        return database.get_messages_since(chatroomID, timesince, channel_ids)


    elif get_method in ['count', 1]:
        # get <count> messages (optionally starting from <time>)

        count = json_data.get('count')
        timebefore = json_data.get('time')

        # set default values
        count = (count if count != None else 10)
            # timebefore defaults to now if we want messages starting from now.
        timebefore = (timebefore if timebefore != None else time.time())


        # make sure variables have the right type
        try:
            count = int(count)
        except Exception as e:
            return f"Could not convert variable 'count' to an integer: {e}", 400

        try:
            timebefore = float(timebefore)
        except Exception as e:
            return f"Could not convert variable 'time' to float: {e}", 400


        return database.get_messages_count(chatroomID, count, timebefore, channel_ids)


    else:
        print('get_method: ',get_method , type(get_method))
        return "Invalid or unset 'get-method'", 400




def create_invite(chatroomID: str, json_data: dict):
    """ Create an invite for a chatroom """

    uses       = json_data.get('uses')
    username     = json_data.get('username')
    expiration_time = json_data.get('expiration-time')

    # placeholder for when classes work
    classID    = None



    # if not set assing default variable, if set then try convert values to their correct types
    try:
        uses = (int(uses) if uses != None else 1)
    except Exception as e:
        return f"Could not convert variable 'uses' to integer: {e}", 400

    try:
        expiration_time = (float(expiration_time) if expiration_time != None else time.time() + 60*60*24*7) 
    except Exception as e:
        return f"Could not convert variable 'expiration-time' to float: {e}", 400


    # NOTE this should be updated when classes and chatroom settings work
    constructor, status = database.get_constructor(chatroomID)
    if status != 200: return constructor, status
    if username !=constructor:
        return "Permission denied: you do not have permission to create an invite", 403


    # save invite
    inviteID, status = database.write_invite(chatroomID, username, classID, expiration_time, uses)
    if status != 200: return inviteID, status


    # create a sharable invite code
    invite_code = f"teahaz:{chatroomID}/{inviteID}"


    return {
            "invite": invite_code,
            "uses": uses,
            "expiration-time": expiration_time,
            "inviteID": inviteID
            }, 200

def use_invite(chatroomID: str, json_data: dict):
    """ Process an invite """

    username = json_data.get('username')
    nickname = json_data.get('nickname')
    password = json_data.get('password')
    inviteID = json_data.get('inviteID')


    # The nickname argument is optional and if not set it will be the same as username
    nickname      = (nickname if nickname != None else username)


    if not security.is_uuid(inviteID):
        return "Invalid invite ID sent to server. Must be uuid!", 400


    required = ['username', 'password', 'inviteID']
    for i, a in enumerate([username, password, inviteID]):
        if a == None or len(a) < 1:
            return f"No value supplied for required field: {required[i]}", 400


    inviteInfo, status = database.get_invite(chatroomID, inviteID)

    if inviteInfo['uses'] < 1:
        return "There are no more uses left on this invite", 403


    if time.time() > inviteInfo['expiration-time']:
        return "Invite has expired", 403


    # decrement uses
    uses = inviteInfo['uses']
    uses = int(uses) - 1

    res, status = database.update_invite(chatroomID, inviteID, inviteInfo['classID'], inviteInfo['expiration-time'],  uses)
    if status != 200: return res, status


    username, status = users.add_user(chatroomID, username, nickname, password)
    if status != 200: return username, status


    return helpers.get_chat_info(chatroomID, username)




def get_users(chatroomID: str, json_data: dict):
    """ Get all users of a chatroom """

    # NOTE maybe later add option to filter by channel, where it only gets users that have permission to view a channel.
    # ofc that would only be available to users that can already view that channel.

    # NOTE this only gets a single user rn, but as there are no invites yet its not a huge problem.
    constructor, status = database.get_constructor(chatroomID)
    if status != 200: return constructor, status


    user_data, status = database.fetch_user(chatroomID, constructor)
    return [user_data], 200




