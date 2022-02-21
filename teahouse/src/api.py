""" Functions almost directly exposed to users """

import time

import users_th as users
import dbhandler as database
import security_th as security
import global_helpers as helpers
import filesystem_th as filesystem


# setup logging
from logging_th import logger
LOG = logger()



# -------------------------------------------------------------------- chatroom -------------------------------------------------------
def create_chatroom(json_data) -> tuple[dict | str, int]:
    """ Create a chatroom """

    # get arguments
    username      = json_data.get('username')
    nickname      = json_data.get('username')
    password      = json_data.get('password')
    chatroom_name = json_data.get('chatroom-name')


    # The nickname argument is optional and if not set it will be the same as username
    nickname      = (nickname if nickname != None else username)


    # generate ID for chatroom
    chatroom_id    = security.gen_uuid()


    # Make sure all arguments are given
    required = ['username', 'password', 'chatroom_name']
    for i, req in enumerate([username, password, chatroom_name]):
        if req == None or len(req) < 1:
            return f"No value supplied for required field: {required[i]}", 400


    # Create folders needed for chatroom
    res, status = filesystem.create_chatroom_folders(chatroom_id)
    if status != 200:
        LOG.error(create_chatroom, "Failed to create chatroom folders!")
        return res, 500


    # Create mongodb database for the catroom
    chatroom_data, status = database.init_chat(chatroom_id, chatroom_name)
    if status != 200:
        LOG.error(create_chatroom, f"Failed to create chatroom database.\n Traceback: {res}")

        # If creating the database fails then remove chatroom folders
        filesystem.remove_chatroom(chatroom_id)
        return chatroom_data, status



    # add the default user to the chatrom
    user_data, status = users.add_user(chatroom_id, username, nickname, password)
    if status != 200:
        return user_data, status


    # add initial message
    message_id, status = database.write_message_event(chatroom_id, "system", { "event_type": "newuser", "user_info": user_data })
    if status != 200:
        return message_id, status

    # no longer using chatroom_data in favour of helpers.get_chat_info
    # chatroom_data['users'] = [user_data]
    # chatroom_data['chatroom_id'] = chatroom_id

    # return information about the created chatroom
    return helpers.get_chat_info(chatroom_id, username)



# -------------------------------------------------------------------- login ----------------------------------------------------------
def login(chatroom_id: str, json_data: dict) -> (dict, int):
    """ Login to chatroom """

    # get arguments
    username   = json_data.get('username')
    password = json_data.get('password')

    # Make sure all arguments are given
    required = ['username', 'password']
    for i, req in enumerate([username, password]):
        if req == None or len(req) < 1:
            return f"No value supplied for required field: {required[i]}", 400

    # authenticate user
    res, status = users.auth_user(chatroom_id, username, password)
    if status != 200:
        return res, status

    # return with useful information about the chatroom
    return helpers.get_chat_info(chatroom_id, username)



# -------------------------------------------------------------------- messages -------------------------------------------------------
def send_message(chatroom_id: str, json_data: dict):
    """ Save message sent from user """

    reply_id   = json_data.get('replyID')
    mtype     = 'text'

    channel_id = json_data.get('channelID')
    username    = json_data.get('username')

    key_id     = None
    mtext     = json_data.get('data')


    # Make sure all arguments are given
    required = ["mtype", "channelID", "username", "data"]
    for i, req in enumerate([mtype, channel_id, username, mtext]):
        if req == None:
            return f"No value supplied for required field: {required[i]}.", 400


    # Validate user input
    values = ["replyID", "channelID"] # , "keyID" ]
    for i, val in enumerate([reply_id, channel_id]):
        if val != None and not security.is_uuid(val):
            return f"Value for {values[i]} is not a valid UUID!", 400


    # users should not be able to send empty messages
    if len(mtext) < 1:
        return "Cannot send empty message", 400


    # Check if channel exists and that the user has access to it
    permissions, status = database.get_channel_permissions(chatroom_id, channel_id, username)
    if status != 200:
        return permissions, status


    if not permissions['w']:
        return "You do not have permissions to write in this channel", 403

    # continue on from here
    return database.write_message_text(chatroom_id, channel_id, username, mtext, reply_id)


def get_messages(chatroom_id: str, json_data: dict):
    """ Get all messages since <time> """

    time = json_data.get('time')
    username = json_data.get('username')
    channel_id = json_data.get('channelID')



    # If channelID is a uuid then only look for messages
    # in that one channel.
    if security.is_uuid(channel_id):
        channels = [{ "channelID": channel_id }]

    # If channelID is not set then look for messages in
    # all readable channels.
    elif channel_id == None:
        channels, status = database.fetch_all_readable_channels(chatroom_id, username)
        if status != 200:
            return channels, status

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
    except Exception as err:
        return f"Could not convert variable 'time' to float: {err}", 400

    # Return messages
    return database.get_messages_since(chatroom_id, timesince, channel_ids)



# -------------------------------------------------------------------- invite --------------------------------------------------------
def create_invite(chatroom_id: str, json_data: dict) -> (dict or str, int):
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
        for cls in classes_unclean:
            classes.append(cls.strip())

    # Classes has to be an array
    if type(classes) != list:
        return "ClassID was set to an invalid value. Must be array or None.", 400

    # Get a list of all valid classIDs
    valid_classes, status = database.fetch_all_classes(chatroom_id)
    if status != 200:
        return valid_classes, status

    valid_class_ids = []
    for cls in valid_classes:
        valid_class_ids.append(cls['classID'])

    # There is no need to add the default class
    #   to each invite as you cannot create a user
    #   in th without having a default class. (dbhandler/write_user)
    if type(classes) == list:

        # Remove all duplilcats from the 
        classes = list(set(classes))

        # make sure all classes are valid
        for class_id in classes:
            if class_id not in valid_class_ids:
                return "One of the values in 'classes' is not a valid classID", 400



    # For now only chatroom admins can creaate invites.
    # I plan on adding more granular permissions were people can have
    #   invite permissions without having to be admins.
    is_admin, status = database.check_permission(chatroom_id, username, "admin")
    if status != 200:
        return is_admin, status


    if is_admin != True:
        return "Permission denied: You dont have permissions to create an invite.", 403

    # save invite
    return  database.write_invite(chatroom_id, username, classes, expiration_time, uses)


def use_invite(chatroom_id: str, json_data: dict):
    """ Process an invite """

    username = json_data.get('username')
    nickname = json_data.get('nickname')
    password = json_data.get('password')
    invite_id = json_data.get('inviteID')


    # The nickname argument is optional and if not set it will be the same as username
    nickname      = (nickname if nickname is not None else username)


    # Make sure all three arguments are there
    required = ['username', 'password', 'inviteID']
    for i, req in enumerate([username, password, invite_id]):
        if req == None or len(req) < 1:
            return f"No value supplied for required field: {required[i]}", 400


    # Make sure invite is a valid uuid
    if not security.is_uuid(invite_id):
        return "Invalid invite ID sent to server. Must be uuid!", 400


    invite_info, status = database.fetch_invite(chatroom_id, invite_id)
    if status != 200:
        return invite_info, status


    if invite_info['uses'] < 1:
        return "There are no more uses left on this invite", 403


    if time.time() > invite_info['expiration_time']/1: # div by one to force a float
        return "Invite has expired", 403


    # decrement uses
    uses = invite_info['uses']
    uses = int(uses) - 1

    # Got this far in writing use_invite.
    # Need to write changes to the invite and some other things


    # IMPORTANT: cba to update invite as im about to re-write most of this.
    # for now the invite just doesnt get decremented
    # print('invite_info: ',invite_info , type(invite_info))
    # res, status = database.update_invite(chatroom_id, invite_id, invite_info['classes'], invite_info['expiration_time'],  uses)
    # if status != 200:
    #     return res, status


    username, status = users.add_user(chatroom_id, username, nickname, password)
    if status != 200:
        return username, status


    return helpers.get_chat_info(chatroom_id, username)



# -------------------------------------------------------------------- channels -------------------------------------------------------
def create_channel(chatroom_id: str, json_data: dict) -> (dict, int):
    """ Create a channel """

    username     = json_data.get('username')
    channel_name = json_data.get('channel-name')
    permissions  = json_data.get('permissions')


    if type(channel_name) != str or len(channel_name) > 200:
        return "Channel_name must be a string that is less than 200 characters long", 400


    admins, status =  helpers.get_admins(chatroom_id)
    if status != 200:
        return admins, status


    if username not in admins:
        return "You do not have permission to create channels", 403


    permissions, status = helpers.sanitize_permission_list(chatroom_id, permissions)
    if status != 200:
        return permissions, status



    channel_obj, status = database.write_channel(chatroom_id, channel_name, permissions)
    if status != 200:
        return channel_obj, status


    return channel_obj, 200
