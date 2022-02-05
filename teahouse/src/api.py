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





# -------------------------------------------------------------------- chatroom -------------------------------------------------------
def create_chatroom(json_data) -> (dict, int):
    """ Create a chatroom """

    # get arguments
    username      = json_data.get('username')
    nickname      = json_data.get('username')
    password      = json_data.get('password')
    chatroom_name = json_data.get('chatroom-name')


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


    # Create mongodb database for the catroom
    chatroom_data, status = database.init_chat(chatroomID, chatroom_name)
    if status != 200:
        log.error(create_chatroom, f"Failed to create chatroom database.\n Traceback: {res}")

        # If creating the database fails then remove chatroom folders
        filesystem.remove_chatroom(chatroomID)
        return chatroom_data, status



    # add the default user to the chatrom
    user_data, status = users.add_user(chatroomID, username, nickname, password)
    if status != 200: return user_data, status


    # add initial message
    messageID, status = database.write_message_event(chatroomID, "system", { "event_type": "newuser", "user_info": user_data })
    if status != 200: return messageID, status

    # no longer using chatroom_data in favour of helpers.get_chat_info
    # chatroom_data['users'] = [user_data]
    # chatroom_data['chatroomID'] = chatroomID

    # return information about the created chatroom
    return helpers.get_chat_info(chatroomID, username)




# -------------------------------------------------------------------- login ----------------------------------------------------------
def login(chatroomID: str, json_data: dict) -> (dict, int):
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

    # return with useful information about the chatroom
    return helpers.get_chat_info(chatroomID, username)




# -------------------------------------------------------------------- messages -------------------------------------------------------
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
    for i, a in enumerate([replyID, channelID]):
        if a != None and not security.is_uuid(a):
            return f"Value for {values[i]} is not a valid UUID!", 400


    # users should not be able to send empty messages
    if len(mtext) < 1:
        return "Cannot send empty message", 400


    # Check if channel exists and that the user has access to it
    permissions, status = database.get_channel_permissions(chatroomID, channelID, username)
    if status != 200: return permissions, status


    if not permissions['w']:
        return "You do not have permissions to write in this channel", 403

    # continue on from here
    return database.write_message_text(chatroomID, channelID, username, mtext, replyID)

def get_messages(chatroomID: str, json_data: dict):
    """ Get all messages since <time> """

    time = json_data.get('time')
    username = json_data.get('username')
    channelID = json_data.get('channelID')



    # If channelID is a uuid then only look for messages
    # in that one channel.
    if security.is_uuid(channelID):
        channels = [{ "channelID": channelID }]

    # If channelID is not set then look for messages in
    # all readable channels.
    elif channelID == None:
        channels, status = database.fetch_all_readable_channels(chatroomID, username)
        if status != 200: return channels, status

    # If neither than channelID is probably not valid.
    else:
        return "ChannelID is set but it is not a valid UUID!", 400


    # fetch_all_readable_channels returns a bunch of data about
    # the chatrooms that is unimportant. Filter to just have the
    # channelIDs in an array.
    channel_ids = []
    for i in channels:
        channel_ids.append(i['channelID'])



    # The 'time' variable has to be either float, or
    # a value that can be converted to float without any issue.
    try:
        timesince = float(time)
    except Exception as e:
        return f"Could not convert variable 'time' to float: {e}", 400

    # Return messages
    return database.get_messages_since(chatroomID, timesince, channel_ids)



# -------------------------------------------------------------------- invite --------------------------------------------------------
def create_invite(chatroomID: str, json_data: dict) -> (dict or str, int):
    """ Create an invite for a chatroom """

    username        = json_data.get('username')

    uses            = json_data.get('uses')
    classes         = json_data.get('classes', [])
    expiration_time = json_data.get('expiration-time')



    # These should be manditory because I dont like
    # setting default values for things.
    for i in ['uses', 'expiration-time']:
        if json_data.get(i) == None:
            return "No value supplied for required argument: {i}", 400



    # make sure uses is a valid int
    try:
        uses = int(uses)
    except ValueError:
        return "'uses' variable is not a valid integer.", 400

    # make sure expiration_time is valid
    try:
        expiration_time = float(expiration_time)
    except ValueError:
        return "'expiration-time' variable is not a valid float.", 400



    # HTML headers do not support sending
    #   arrays. For now instead we send a
    #   comma seperated list or define
    #   the header multiple times as flask
    #   will interpret them both the same.
    if type(classes) == str:
        classes_unclean = classes.split(',')
        classes = []
        for c in classes_unclean:
            classes.append(c.strip())

    # Classes has to be an array
    if type(classes) != list:
        return "ClassID was set to an invalid value. Must be array or None.", 400

    # Get a list of all valid classIDs
    valid_classes, status = database.fetch_all_classes(chatroomID)
    if status != 200: return valid_classes, status

    valid_classIDs = []
    for c in valid_classes:
        valid_classIDs.append(c['classID'])

    # There is no need to add the default class
    #   to each invite as you cannot create a user
    #   in th without having a default class. (dbhandler/write_user)
    if type(classes) == list:

        # Remove all duplilcats from the 
        classes = list(set(classes))

        # make sure all classes are valid
        for classID in classes:
            if classID not in valid_classIDs:
                return "One of the values in 'classes' is not a valid classID", 400



    # For now only chatroom admins can creaate invites.
    # I plan on adding more granular permissions were people can have
    #   invite permissions without having to be admins.
    is_admin, status = database.check_permission(chatroomID, username, "admin")
    if status != 200: return is_admin, status


    if is_admin != True:
        return "Permission denied: You dont have permissions to create an invite.", 403

    # save invite
    return  database.write_invite(chatroomID, username, classes, expiration_time, uses)

def use_invite(chatroomID: str, json_data: dict):
    """ Process an invite """

    username = json_data.get('username')
    nickname = json_data.get('nickname')
    password = json_data.get('password')
    inviteID = json_data.get('inviteID')


    # The nickname argument is optional and if not set it will be the same as username
    nickname      = (nickname if nickname != None else username)


    required = ['username', 'password', 'inviteID']
    for i, a in enumerate([username, password, inviteID]):
        if a == None or len(a) < 1:
            return f"No value supplied for required field: {required[i]}", 400


    if not security.is_uuid(inviteID):
        return "Invalid invite ID sent to server. Must be uuid!", 400


    invite_info, status = database.fetch_invite(chatroomID, inviteID)
    if status != 200: return invite_info, status


    if invite_info['uses'] < 1:
        return "There are no more uses left on this invite", 403


    if time.time() > invite_info['expiration_time']/1: # div by one to force a float
        return "Invite has expired", 403


    # decrement uses
    uses = invite_info['uses']
    uses = int(uses) - 1

    # Got this far in writing use_invite.
    # Need to write changes to the invite and some other things

    res, status = database.update_invite(chatroomID, inviteID, invite_info['classID'], invite_info['expiration_time'],  uses)
    if status != 200: return res, status


    username, status = users.add_user(chatroomID, username, nickname, password)
    if status != 200: return username, status


    return helpers.get_chat_info(chatroomID, username)




# -------------------------------------------------------------------- channels -------------------------------------------------------
def create_channel(chatroomID: str, json_data: dict) -> (dict, int):
    """ Create a channel """

    username     = json_data.get('username')
    channel_name = json_data.get('channel-name')
    permissions  = json_data.get('permissions')


    if type(channel_name) != str or len(channel_name) > 200:
        return "Channel_name must be a string that is less than 200 characters long", 400


    admins, status =  helpers.get_admins(chatroomID)
    if status != 200: return admins, status


    if username not in admins:
        return "You do not have permission to create channels", 403


    permissions, status = helpers.sanitize_permission_list(chatroomID, permissions)
    if status != 200: return permissions, status



    channel_obj, status = database.write_channel(chatroomID, channel_name, permissions)
    if status != 200: return channel_obj, status


    return channel_obj, 200




