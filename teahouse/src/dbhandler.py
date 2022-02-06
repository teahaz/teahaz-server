"""
    Module handles interacting with the database.
    Things outside this file should not touch the
    db and all functions here must have something
    to do with the database.
"""


import os
import time
import pymongo
import sqlite3

import security_th as security
import global_helpers as helpers

# setup logging
from logging_th import logger
LOG = logger()


# make mongodb connection
mongodb = pymongo.MongoClient('mongodb', 27017)


def _gethandle(chatroomID: str):
    if not security.is_uuid(chatroomID):
        return "ChatroomID is not a valid uuid", 400
    return mongodb[chatroomID], 200


class database():
    """ Abstraction over database functions """


    # NOTE possible security improvement.
    # We could have all the tables and their values defined
    #   in a dict as an instance variable of this object.

    # This would both make it simpler to init_chat and
    #   it would mean that we can valiedate some data before executing it.


    def __init__(self, chatroomID: str):
        LOG.warn(database, "Depricated database used!")

        # cant return in __init__ but make sure that invalid uuid's are not being used
        assert(security.is_uuid(chatroomID))

        if not os.path.exists(f'storage/chatrooms/{chatroomID}'):
            self.exists = False
        else:
            self.exists = True

        self.chatroomID = chatroomID
        self.db = sqlite3.connect(f'storage/chatrooms/{chatroomID}/main.db')

    def _run(self, statement: str, variables: tuple = ()):
        """ Internal function to run sql statements """
        try:
            cursor = self.db.cursor()
            cursor.execute(statement, variables)
            return cursor, 200

        except Exception as e:
            LOG.error(self._run, f"Database operation failed: {e}")
            return f"Database operation failed: {e}", 500


    def close(self):
        """
            Close database.

            This method MUST be run after using the database
        """
        self.db.close()

    def commit(self):
        """ Saves changes to a database """
        self.db.commit()


    def create(self, table: str, values: list):
        """ Wrapper around creating tables """

        values = str(values).strip('[').strip(']')
        statement = f"CREATE TABLE {table} ({values})"

        status= self._run(statement)[1]

        if status != 200:
            # we can raise here because this will only ever be called internally with internal arguments
            raise f"Failed to create table: {table}"


    def select(self, what: str, table: str, conditions: str = '', variables: tuple = ()):
        """ Wrapper around getting data from the database """

        statement = f"SELECT {what} FROM {table} WHERE {conditions}"

        # if no conditions were set, get all
        if len(conditions) == 0:
            statement = f"SELECT {what} FROM {table}"


        cursor, status= self._run(statement, variables)
        if status != 200:
            return cursor, status

        data = cursor.fetchall()
        return data, 200


    def insert(self, table: str, values: tuple):
        """ Wrapper around adding data to the database """

        # Get (?, ?, ?) like syntax
        rowcount = len(values)
        row = "(" + ("?, "*rowcount).strip(', ') + ")"

        # run
        statement = f"INSERT INTO {table} VALUES {row}"
        return self._run(statement, values)


    def update(self, table: str, what: list, values: tuple, conditions: str):
        """ Wrapper around sql update statement """

        # user can add conditions that need to be updated in a list of strings.
        values_to_update = ''
        for i in what:
            values_to_update += i + "=?, "
        # get rid of last comma
        values_to_update = values_to_update.strip(', ')


        statement = f"UPDATE {table} SET {values_to_update} WHERE {conditions}"
        return self._run(statement, values)



#-------------------------------------------------------------- Chatroom -----------------------
def init_chat(chatroomID: str, chat_name: str):
    """ Creating a mongodb database for a new chatroom """
    LOG.log(init_chat, f"Creating chatroom {chatroomID}")

    # This line should get a handle for the new database.
    # note: mongodb doesnt actually create the database,
    #   or any collections until the first document is inserted into them.
    db = mongodb[chatroomID]


    # insert constructor and default class
    class_collection = db.classes
    default_classes = [
        {
            "_id": "0",
            "public":
            {
                "classID": "0",
                "name": "constructor",
                "admin": True
            }
        },
        {
            "_id": "1",
            "public":
            {
                "classID": "1",
                "name": "default",
                "admin": False
            }
        }]
    class_collection.insert_many(default_classes)


    # Add the default channel
    channelID = security.gen_uuid()
    channel_collection = db.channels
    default_channel = {
            "_id": channelID,
            "public":
            {
                "channelID": channelID,
                "name": "default",
                "permissions":
                [
                    {
                        "classID": "1",
                        "r": True,
                        "w": True,
                        "x": False
                    }
                ]
            }
        }
    channel_collection.insert_one(default_channel)


    # Add some default settings
    chatroom_collection = db.chatroom
    default_settings = {
            "_id": str(chatroomID),
            "public":
            {
                "settings":
                [
                    {
                        "sname": "chatroom_name",
                        "svalue": str(chat_name),
                        "stype": "string"
                    },
                    {
                        "sname": "min_password_length",
                        "svalue": 10,
                        "stype": "int"
                    },
                    {
                        "sname": "default_channel",
                        "svalue": channelID,
                        "stype": "string"
                    }
                ]
            }
        }
    chatroom_collection.insert_one(default_settings)


    # collect data for returning to the user
    chatroom_data = {
            "channels": [default_channel['public']],
            "settings": default_settings['public']['settings'],
            "classes":
            [
                default_classes[0]['public'],
                default_classes[1]['public']
            ]
        }

    return chatroom_data, 200


def check_settings(chatroomID: str, setting_name: str):
    """ Fetch the setting value corresponding to a setting name from database"""

    db, status = _gethandle(chatroomID)
    if status != 200:
        return db, status

    document = db.chatroom.find_one()
    settings = document['public']['settings']

    for setting in settings:
        if setting.get('sname') == setting_name:
            return setting.get('svalue'), 200

    return "No such setting", 400


def fetch_all_settings(chatroomID: str):
    """ Get all settings of a chatroom """

    db, status = _gethandle(chatroomID)
    if status != 200:
        return db, status

    document = db.chatroom.find_one()
    settings = document['public']['settings']

    settings_list = []
    for setting in settings:
        settings_list.append(setting)

    return settings_list, 200



#-------------------------------------------------------------- Messages -----------------------
def write_message_event(chatroomID: str, mtype: str, data: dict) -> (dict or str, int):
    """ Write an event into the messages collection """

    # just make sure that I am using this function correctly
    assert(mtype not in ['text', 'file'])

    # get db
    db, status = _gethandle(chatroomID)
    if status != 200:
        return db, status

    # randomly generate an id for the message
    messageID = security.gen_uuid()

    # format message
    message_obj ={
            "_id": messageID,
            "public":
            {
                "messageID": messageID,
                "time": time.time(),
                "type": str(mtype),
                "data": data
            }
        }

    # add to database
    db.messages.insert_one(message_obj)

    return message_obj['public'], 200


def write_message_text(chatroomID: str, channelID: str, username: str, message: str, replyID: str = None) -> (dict or str, int):
    """ Write a message inot the messages field """

    db, status = _gethandle(chatroomID)
    if status != 200:
        return db, status

    # randomly generate an id for the message
    messageID = security.gen_uuid()

    # format message
    message_obj ={
            "_id": messageID,
            "public":
            {
                "messageID": messageID,
                "time": time.time(),
                "channelID": channelID,
                "username": username,
                "type": 'text',
                "data": message
            }
        }

    # If there is a replyID is set then add then change the message
    # from a standard text to a reply.
    if replyID != None:
        message_obj['public']['type'] = 'reply-text'
        message_obj['public']['replyID'] = replyID


    db.messages.insert_one(message_obj)
    return message_obj['public'], 200


def get_messages_since(chatroomID: str, timesince: float, channels_to_look_in: list) -> (list or str, int):
    """ Get all messages since {timesince} from channels specified by {channels_to_look_in} """

    # get db
    db, status = _gethandle(chatroomID)
    if status != 200:
        return db, status


    # Make a query for mongodb.
    # The query should get all messages that:
    #   - have been sent since the <timesince> variable
    #           (epoch time)
    #   - Is either a system message or is in one of
    #       of the channels in the channels_to_look_in variable
    query = {
            "$and":
            [
                {"public.time": { "$gte": timesince }},
                {"$or":
                [
                    {"public.type": {"$in": helpers.system_message_types}},
                    {"public.channelID": {"$in": channels_to_look_in}}
                ]}
            ]
    }

    # Loop over the messages iterator and return an array.
    messages = [m['public'] for m in db.messages.find(query)]
    return messages, 200



#-------------------------------------------------------------- Channels -----------------------
def write_channel(chatroomID: str, channel_name: str, permissions: list) -> (dict or str, int):
    """ Add new channel to database """

    # generate channelID
    channelID = security.gen_uuid()

    # insert into db
    db, status = _gethandle(chatroomID)
    if status != 200:
        return db, status

    channel_data = {
            "_id": channelID,
            "public":
                {
                    "channelID": channelID,
                    "name": channel_name,
                    "permissions": permissions
                }
            }

    db.channels.insert_one(channel_data)

    return channel_data['public'], 200


def fetch_channel(chatroomID: str, channelID: str, include_private=False) -> (dict, int):
    """ Fetch all information about a channel """

    db, status= _gethandle(chatroomID)
    if status != 200:
        return db, status

    channel = db.channels.find_one({'_id': channelID})
    if not channel:
        return "Channel not found", 404

    if not include_private:
        channel = channel['public']

    return channel, 200


def fetch_all_channels(chatroomID: str, include_private=False) -> (list or str, int):
    """ Get a list of all channels """

    db, status= _gethandle(chatroomID)
    if status != 200:
        return db, status

    channels = []
    for d in db.channels.find():
        if include_private:
            channels.append(d)
        else:
            channels.append(d['public'])

    return channels, 200


def get_channel_permissions(chatroomID: str, channelID: str, username: str) -> (dict or str, int):
    """
        Gets channel permissions from the perspective of the user.

        ie: it gets the what the user can do in a channel
    """

    db, status = _gethandle(channelID)
    if status != 200:
        return db, status

    user, status = fetch_user(chatroomID, username)
    if status != 200:
        return user, status

    admins, status = helpers.get_admins(chatroomID)
    if status != 200:
        return admins, status

    # if a user is an admin (including the constructor) he has access to everything
    if user['username'] in admins:
        return {
                "r": True,
                "w": True,
                "x": True,
                }, 200


    channel, status = fetch_channel(chatroomID, channelID)
    if status != 200:
        return channel, status

    # set up defautls that will be changed
    permissions = {
            "r": False,
            "w": False,
            "x": False,
            }

    # loop through all classes and get the highest better permission of each
    for p in channel['permissions']:
        if p['classID'] in user['classes']:
            if p['r'] == True:
                permissions['r'] = True
            if p['w'] == True:
                permissions['w'] = True
            if p['x'] == True:
                permissions['x'] = True


    return permissions, 200



def can_read(chatroomID: str, channelID: str, username: str) -> (bool, int):
    """
        Checks if a user can read a channel.

        As this returns on the first read permission,
        it should be on average a lot faster than
        get_channel_permissions that would have to take into
        account all classes and permissions.
    """

    # get user info
    user, status = fetch_user(chatroomID, username)
    if status != 200:
        return user, status


    # check if user is constructor
    if '0' in user['classes']:
        return True, 200


    # check if user is admin
    classes, status = fetch_all_classes(chatroomID)
    if status != 200:
        return classes, status

    for c in classes:
        if c['admin'] == True and c['classID'] in user['classes']:
            return True, 200


    # get channel info
    channels, status = fetch_channel(channelID, channelID)
    if status != 200:
        return channels, status


    for c in user['classes']:
        for p in channels['permissions']:
            if c == p['classID'] and p['r'] == True:
                return True, 200

    return False, 200


def fetch_all_readable_channels(chatroomID: str, username: str):
    """ Gets a list of all channels that are readable to the user.  """

    channels, status = fetch_all_channels(chatroomID)
    if status != 200:
        return channels, status

    readable_channels = []
    for channel in channels:
        if can_read(chatroomID, channel['channelID'], username)[0]:
            readable_channels.append(channel)

    return readable_channels, 200



#-------------------------------------------------------------- Users -----------------------
def write_user(chatroomID: str, username: str, nickname: str, password: str):
    """ write user to database """


    db, status = _gethandle(chatroomID)
    if status != 200:
        return db, status


    # hash password
    password = security.hashpw(password)

    user_data = {
            "_id": str(username),
            "private":
            {
                "password": password,
                "cookies": []
            },
            "public":
            {
                "username": str(username),
                "nickname": str(nickname),
                "colour":
                {
                    "r": None,
                    "g": None,
                    "b": None,
                },
                "classes": []
            }
        }


    # if this is the first user in the chatroom then make them the constructor
    first_user = db.users.find_one()
    if not first_user:
        user_data['public']['classes'].append('0')

    # assing the default class to the user
    user_data['public']['classes'].append('1')


    # make sure someone with the same username doesnt already exist
    if db.users.find_one({"_id": str(username)}) != None:
        return "A user with this username already exists", 400


    db.users.insert_one(user_data)
    return user_data['public'], 200


def fetch_user(chatroomID: str, username: str, include_private=False) -> (dict or str, int):
    """
        Fetch all public information about a user

        This is just a shorthand for only getting
        the public info from fetch_user().
    """

    db, status = _gethandle(chatroomID)
    if status != 200:
        return db, status

    user_data = db.users.find_one({'_id': username})

    if not user_data:
        return "User not found", 404

    if not include_private:
        user_data = user_data['public']

    return user_data, 200


def fetch_all_users(chatroomID:str):
    """ Fetch all users (members) of a chatroom """

    db, status = _gethandle(chatroomID)
    if status != 200:
        return db, status

    users = []
    for d in db.users.find():
        users.append(d['public'])

    return users, 200


def check_permission(chatroomID: str, username: str, permission_name: str) -> (bool or str, int):
    """
        With permission name supplied to something like 'admin',
        the function checks whether or not the user has any class
        where this is set to 'true'.

        Note: any true value overwrites all other non-true value,
        so the user only needs this permission from any one class.
    """
    user_data, status = fetch_user(chatroomID, username)
    if status != 200:
        return user_data, status

    for classID in user_data['classes']:
        class_data, status = fetch_class(chatroomID, classID)
        if status != 200:
            return "Internal database error: User classes are corrupt", 500

        # return on the first true
        if class_data[permission_name] == True:
            return True, 200

    # if It didnt find any true value, then return false
    return False, 200



#-------------------------------------------------------------- Cookies -----------------------
def store_cookie(chatroomID: str, username: str, cookie: str):
    """ Writes a cookie to the database """

    db, status = _gethandle(chatroomID)
    if status != 200:
        return db, status

    db.users.update_one({'_id': username}, {'$addToSet': {'private.cookies': cookie}})

    return "OK", 200

def get_cookies(chatroomID: str, username: str, cookie: str):
    """ Get all cookies associated with a user. """

    db, status = _gethandle(chatroomID)
    if status != 200:
        return db, status

    cookies = db.users.find_one({'_id': username}).get('private').get('cookies')
    if cookie == None:
        return "No cookies found!", 404

    return cookies, 200



#-------------------------------------------------------------- Invites -----------------------
def write_invite(chatroomID: str, username: str, classes: list, expiration_time: float, uses: int) -> (dict or str, int):
    """
        Generate an invite and save it in the database

        Return Values:
            - if ok: Public part of object that got written to the db., status_code
            - else: error string, status_code
    """

    print('uses: ',uses , type(uses))

    inviteID = security.gen_uuid()

    db, status = _gethandle(chatroomID)
    if status != 200:
        return db, status

    invite_obj = {
            "_id": inviteID,
            "public":
            {
                "inviteID": inviteID,
                "username": username,

                "uses": uses,
                "classes": classes,
                "expiration_time": expiration_time,
            }
        }

    db.invites.insert_one(invite_obj)
    return invite_obj['public'], 200


def fetch_invite(chatroomID: str, inviteID: str) -> dict:
    """ Get all stored information about an invite """

    db, status = _gethandle(chatroomID)
    if status != 200:
        return db, status

    document = db.invites.find_one({"_id": inviteID})
    print('document: ',document , type(document))
    if document == None:
        return "Could not find valid invite with that inviteID'", 404

    return document['public'], 200


def update_invite(chatroomID: str, inviteID: str, classID: str, expiration_time: float, uses: int):
    """ Update information stored on invite """

    # Force variables to be the right type
    #  this is just a check for myself,
    #  the server should check user input before dbhandler.
    uses = int(uses)
    expiration_time = float(expiration_time)

    db = database(chatroomID)

    res, status = db.update(
            'invites',
            ["classID", "expiration_time", "uses"],
            (classID, expiration_time, uses, inviteID),
            "inviteID=?"
            )
    if status != 200:
        return "Internal database error while updateing invite", 500

    db.commit()
    db.close()
    return "OK", 200



#-------------------------------------------------------------- Classes -----------------------
def get_constructor(chatroomID: str):
    """ 
        Simple, fast function for gettitng the chatroom constructor

        return:
            username, status
    """

    db = database(chatroomID)

    constructor, status = db.select('username', 'userclasses', 'classID=?', ('0',))
    if status != 200:
        return constructor, status

    return constructor[0][0], 200


def fetch_all_classes(chatroomID: str) -> (dict or str, int):
    """ Gets all classes of a chatroom. """

    db, status = _gethandle(chatroomID)
    if status != 200:
        return db, status

    classes = []
    for d in db.classes.find():
        classes.append(d['public'])

    return classes, 200


def fetch_class(chatroomID: str, classID: str) -> (dict or str, int):
    """ Fetch all information about a class """

    if classID not in ['0', '1'] and not security.is_uuid(classID):
        return "Invalild classID was supplied", 500

    db, status = _gethandle(chatroomID)
    if status != 200:
        return db, status

    class_data = db.classes.find_one({'_id': classID})
    if class_data == None:
        return "No such class", 500

    return class_data['public'], 200
