import os
import time
import pymongo
import sqlite3
from pprint import pprint

import security_th as security
import global_helpers as helpers

# setup logging
from logging_th import logger
global log
log = logger()


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
        log.warn(database, "Depricated database used!")

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
            log.error(self._run, f"Database operation failed: {e}")
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
    log.log(init_chat, f"Creating chatroom {chatroomID}")

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
    if status != 200: return db, status

    document = db.chatroom.find_one()
    settings = document['public']['settings']

    for setting in settings:
        if setting.get('sname') == setting_name:
            return setting.get('svalue'), 200

    return "No such setting", 400

def fetch_all_settings(chatroomID: str):
    """ Get all settings of a chatroom """

    db, status = _gethandle(chatroomID)
    if status != 200: return db, status

    document = db.chatroom.find_one()
    settings = document['public']['settings']

    settings_list = []
    for setting in settings:
        settings_list.append(setting)

    return settings_list, 200




#-------------------------------------------------------------- Messages -----------------------
def write_message_event(chatroomID: str, mtype: str, data: dict):
    """ Write message into the messages collection """

    # get db
    db, status = _gethandle(chatroomID)
    if status != 200: return db, status

    # get id and time
    messageID = security.gen_uuid()


    # get default channel
    channelID, status = check_settings(chatroomID, "default_channel")
    if status != 200:
        return f"Internal database error while getting default channel {channelID}", 500

    # format message
    message_obj ={
            "_id": messageID,
            "private":
            {
                "chanread":
                [
                    '1' # can read 1 means that this message can be read by everyone
                ]
            },
            "public":
            {
                "messageID": messageID,
                "time": time.time(),
                "type": str(mtype),
                "action": "hey"
            }
        }

    # add to database
    db.messages.insert_one(message_obj)

    return message_obj['public'], 200

def get_messages_count(chatroomID: str, count: int, timebefore: float, channels_to_look_in: list):
    """ Get {count} amount of messages starting from {timebefore} from channels specified by {channels_to_look_in}.  """

    # get db
    db = database(chatroomID)


    # conditions = "channelID = ?" * len(channels_to_look_in)
    conditions = []
    for i in channels_to_look_in:
        conditions.append("channelID = ?")
    conditions = " OR ".join(conditions)


    # add all variables to a tuple
    variables = (timebefore,)
    for i in channels_to_look_in:
        variables += (i,)
    variables += (count,)


    res, status = db._run(f"SELECT * FROM messages WHERE mtime <= ? AND ({conditions}) ORDER BY mtime DESC LIMIT ?", variables)
    if status != 200: return res, status

    return helpers.db_format_message(res.fetchall())

def get_messages_since(chatroomID: str, timesince: float, channels_to_look_in: list):
    """ Get all messages since {timesince} from channels specified by {channels_to_look_in} """

    db = database(chatroomID)

    # conditions = "channelID = ?" * len(channels_to_look_in)
    conditions = []
    for i in channels_to_look_in:
        conditions.append("channelID = ?")
    conditions = " OR ".join(conditions)


    # add all variables to a tuple
    variables = (timesince,)
    for i in channels_to_look_in:
        variables += (i,)


    cursor, status = db._run(f"SELECT * FROM messages WHERE mtime >= ? AND ({conditions}) ORDER BY mtime DESC LIMIT 100", variables)
    if status != 200: return cursor, status

    return helpers.db_format_message(cursor.fetchall())






#-------------------------------------------------------------- Channels -----------------------
def write_channel(chatroomID: str, channel_name: str, permissions: list) -> (dict or str, int):
    """ Add new channel to database """

    # generate channelID
    channelID = security.gen_uuid()

    # insert into db
    db, status = _gethandle(chatroomID)
    if status != 200: return db, status

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
    if status != 200: return db, status

    channel = db.channel.find_one({'_id': channelID})
    if not channel:
        return "Channel not found", 404

    if not include_private:
        channel = channel['public']

    return channel, 200



def fetch_all_channels(chatroomID: str, include_private=False) -> (list, int):
    """ Get a list of all channels """

    db, status= _gethandle(chatroomID)
    if status != 200: return db, status

    channels = []
    for d in db.channels.find():
        if include_private:
            channels.append(d)
        else:
            channels.append(d['public'])

    return channels, 200


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
    if status != 200: return user, status


    # check if user is constructor
    if '0' in user['classes']:
        return True, 200


    # check if user is admin
    classes, status = fetch_all_classes(chatroomID)
    if status != 200: return classes, status

    for c in classes:
        if c['admin'] == True and c['classID'] in user['classes']:
            return True, 200


    # get channel info
    channels, status = fetch_channel(channelID, channelID)
    if status != 200: return channels, status


    for c in user['classes']:
        for p in channels['permissions']:
            if c == p['classID'] and p['r'] == True:
                return True, 200

    return False, 200



def fetch_all_readable_channels(chatroomID: str, username: str):
    """ Gets a list of all channels that are readable to the user.  """

    channels, status = fetch_all_channels(chatroomID)
    if status != 200: return channels, status

    readable_channels = []
    for channel in channels:
        if can_read(chatroomID, channel['channelID'], username)[0]:
            readable_channels.append(channel)

    return readable_channels, 200






#-------------------------------------------------------------- Users -----------------------
def write_user(chatroomID: str, username: str, nickname: str, password: str):
    """ write user to database """


    db, status = _gethandle(chatroomID)
    if status != 200: return db, status


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


def fetch_user(chatroomID: str, username: str, include_private=False):
    """
        Fetch all public information about a user

        This is just a shorthand for only getting
        the public info from fetch_user().
    """

    db, status = _gethandle(chatroomID)
    if status != 200: return db, status

    user_data = db.users.find_one({'_id': username})

    if not user_data:
        return "User not found", 404

    if not include_private:
        user_data = user_data['public']

    return user_data, 200


def fetch_all_users(chatroomID:str):
    """ Fetch all users (members) of a chatroom """

    db, status = _gethandle(chatroomID)
    if status != 200: return db, status

    users = []
    for d in db.users.find():
        users.append(d['public'])

    return users, 200






#-------------------------------------------------------------- Cookies -----------------------
def store_cookie(chatroomID: str, username: str, cookie: str):
    """ Writes a cookie to the database """

    db, status = _gethandle(chatroomID)
    if status != 200: return db, status

    db.users.update_one({'_id': username}, {'$addToSet': {'private.cookies': cookie}})

    return "OK", 200


def get_cookies(chatroomID: str, username: str, cookie: str):
    """ Get all cookies associated with a user. """

    db, status = _gethandle(chatroomID)
    if status != 200: return db, status

    cookies = db.users.find_one({'_id': username}).get('private').get('cookies')
    if cookie == None:
        return "No cookies found!", 404

    return cookies, 200





#-------------------------------------------------------------- Invites -----------------------
def write_invite(chatroomID: str, username: str, classID: str, expiration_time: float, uses: int):
    """ Generates invite and saves it in the invites databased """

    inviteID = security.gen_uuid()

    db = database(chatroomID)

    status = db.insert('invites', (inviteID, username, classID, expiration_time, uses))[1]
    if status != 200:
        return "Internal database error while saving invite", 500

    db.commit()
    db.close()
    return inviteID, 200

def get_invite(chatroomID: str, inviteID: str) -> dict:
    """ Get all stored information about an invite """

    db = database(chatroomID)

    inviteData, status = db.select('*', 'invites', 'inviteID=?', (inviteID,))
    if status != 200:
        return "Internal database error while reading invites", 500

    if len(inviteData) < 1:
        return "Invite not found", 404

    # format invite data
    try:
        inviteData = inviteData[0]

        inviteData = {
                "inviteID":        inviteData[0],
                "username":          inviteData[1],
                "classID":         inviteData[2],
                "expiration-time": inviteData[3],
                "uses":            inviteData[4]
                }

    except Exception as e:
        return "Internal server error while formatting getting invite information.", 500


    db.close()
    return inviteData, 200

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
    if status != 200: return constructor, status

    return constructor[0][0], 200

def fetch_all_classes(chatroomID: str) -> (dict, int):
    """ Gets all classes of a chatroom. """

    db, status = _gethandle(chatroomID)
    if status != 200: return db, status

    classes = []
    for d in db.classes.find():
        classes.append(d['public'])

    return classes, 200


