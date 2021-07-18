import os
import time
import pymongo
import sqlite3

import security_th as security
import global_helpers as helpers

# setup logging
from logging_th import logger
global log
log = logger()


# make mongodb connection
mongodb = pymongo.MongoClient('mongodb', 27017)



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
        print('statement: ',statement , type(statement))
        return self._run(statement, values)







#-------------------------------------------------------------- Chatroom -----------------------
def init_chat_mongo(chatroomID: str, chat_name: str):
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
            "private":
            {
                "admin": True
            },
            "public":
            {
                "_id": "0",
                "name": "constructor"
            }
        },
        {
            "_id": "1",
            "private":
            {
                "admin": False
            },
            "public":
            {
                "_id": "1",
                "name": "default"
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
                "_id": channelID,
                "name": "default",
                "permissions":
                {
                    {
                        "_id": "1",
                        "r": True,
                        "w": True,
                        "x": False
                    }
                }
            }
        }
    channel_collection.insert_one(default_channel)


    # Add some default settings
    settings_collection = db.settings
    default_settings = [
            {
                "_id": "chatroom_name",
                "public":
                {
                    "sname": "chatroom_name",
                    "svalue": chat_name,
                    "stype": "int"
                }
            },
            {
                "_id": "min_password_length",
                "public":
                {
                    "sname": "min_password_length",
                    "svalue": chat_name,
                    "stype": "int"
                }
            }
        ]
    settings_collection.insert_many(default_settings)


    # collect data for returning to the user
    chatroom_data = {
            "channels": default_channel['public'],
            "settings":
            [
                    default_settings[0]['public'],
                    default_settings[1]['public']
            ],
            "classes":
            [
                default_classes[0]['public'],
                default_classes[1]['public']
            ]
        }

    return chatroom_data, 200





def init_chat(chatroomID: str, chat_name: str):
    """ Create chatroom database and add tables """
    log.log(init_chat, f"Creating chatroom {chatroomID}")

    # Get db object
    db = database(chatroomID)
    if not db.exists:
        return f"Chatroom: {chatroomID}, does not exist!", 404


    # add tables
    db.create('settings',    ['sname',   'svalue', 'stype'])
    db.create('invites',     ['inviteID', 'username', 'classID', 'expiration_time', 'uses'])

    db.create('users',       ['username',  'nickname', 'password'])
    db.create('colours',     ['username',  'r', 'g', 'b'])
    db.create('cookies',     ['username',  'cookie'])

    db.create('classes',     ['classID', 'classname'])
    db.create('userclasses', ['classID', 'username'])

    db.create('channels',    ['channelID', 'channelname',  'public'])
    db.create('permissions', ['channelID', 'classID', 'r', 'w', 'x'])

    db.create('messages',    ['messageID', 'channelID', 'username', 'replyID', 'keyID', 'mtime', 'mtype', 'data'])
    db.create('files',       ['fileID', 'filename', 'size'])


    # Add 'default' to channels
    channelID = security.gen_uuid()
    assert(db.insert('channels', (channelID, 'default', True))[1] == 200)

    # Add default settings
    assert(db.insert('settings', ('chat_name', chat_name, "str"))[1] == 200)
    assert(db.insert('settings', ('min_password_length', 10, "int"))[1] == 200)

    # Add constructor class
    assert(db.insert('classes', ('0', "constructor"))[1] == 200)

    db.commit()
    db.close()
    return {"channelID": channelID, "channel_name": 'default'}, 200



















def check_settings(chatroomID: str, setting_name: str):
    """ From settings table fetch setting value corresponding to supplied setting name """

    db = database(chatroomID)

    data, status = db.select('svalue', 'settings', 'sname=?', (setting_name,))
    if status != 200:
        return "Internal database error while checking settings", status

    if len(data) < 1:
        return f"Setting '{setting_name}' does not exist!", 404


    db.close()
    return data[0][0], 200


def fetch_all_settings(chatroomID: str):
    """ Get all settings of a chatroom """

    db = database(chatroomID)

    data, status = db.select('*', 'settings')
    if status != 200:
        return "Internal database error while getting settings", status


    formatted_setttings = []
    for setting in data:
        formatted = {
                "sname":  setting[0],
                "svalue": setting[1],
                "stype":  setting[2]
                }

        formatted_setttings.append(formatted)

    return formatted_setttings, 200



#-------------------------------------------------------------- Messages -----------------------
def write_message(chatroomID: str, channelID: str, username: str, replyID: str, keyID: str, mtype: str, data: str):
    """ Write message into the messages table """

    # get db
    db = database(chatroomID)

    # get id and time
    mtime = time.time()
    messageID = security.gen_uuid()


    # write message
    status = db.insert("messages", (messageID, channelID, username, replyID, keyID, mtime, mtype, data))[1]
    if status != 200:
        return "Failed to write message.", 500

    db.commit()
    db.close()

    # Client guy asked for the same message formatting as get returns,
    #  might as well use the same function.
    return helpers.db_format_message([(messageID, channelID, username, replyID, keyID, mtime, mtype, data)]), 200

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
def add_channel(chatroomID: str, channel_name: str, is_public: bool):
    """
        Add new channel to database

        return:
            channelID, status
    """

    # generate channelID
    channelID = security.gen_uuid()

    # insert into db
    db = database(chatroomID)
    res, status = db.insert('channels', (channelID, channel_name, is_public))
    if status != 200:
        return res, status


    db.commit()
    db.close()
    return channelID, 200

def fetch_channel(chatroomID: str, channelID: str):
    """
        If channel exists, the function tries to get information about it.

        return:
        {
            channelID: "ID",       : str
            channel_name: "name",  : str
            public: True           : bool
        }, status
    """

    # get db
    db = database(chatroomID)

    # get info on chatroom
    info, status = db.select("*", "channels", "channelID=?", (channelID,))
    if status != 200:
        return "Internal database error, failed to stat channel.", 500


    # check if channel exists
    if len(info) < 1:
        return "Channel does not exist", 404


    db.close()
    return helpers.db_format_channel(info[0])

def fetch_all_channels(chatroomID: str):
    """ Get a list of all channels """

    # get db
    db = database(chatroomID)

    db_response, status = db.select("*", "channels")
    if status != 200:
        return "Internal database error while fetching channels", 500

    channels_list = []
    for i in db_response:
        channel_obj, status = helpers.db_format_channel(i)
        if status != 200:
            return channel_obj, status
        channels_list.append(channel_obj)

    return channels_list, 200

def get_channel_permissions(chatroomID: str, channelID: str, username: str):
    """
        Attempts to get permission information on a channel from the perspective of a specified user.


        return:
        {
            channelID: "ID",       : str
            channel_name: "name",  : str
            permissions:
                {
                    r: True,       : bool
                    w: True,       : bool
                    x: False       : bool
                }
        }, status
    """
    # get db
    db = database(chatroomID)

    # get channel info
    channel_obj, status = fetch_channel(chatroomID, channelID)
    if status != 200:
        return channel_obj, status


    # default chat perms, for public channel
    toret = {
        "channelID": channel_obj.get('channelID'),
        "channel_name": channel_obj.get('channel_name'),
        "public": channel_obj.get('public'),
        "permissions":
            {
                "r": True,
                "w": True,
                "x": False
            }
    }

    # check if user is the constructor of the chatroom, because he can then read everything
    constructor, status = db.select('username', 'userclasses', 'classID=?', ('0',))
    if status != 200: return constructor, status
    constructor = constructor[0][0]
    if constructor == username:
        toret['permissions']['x'] = True
        return toret, 200


    if channel_obj.get('public') == False:
        toret['permissions']['r'] = False
        toret['permissions']['w'] = False
        toret['permissions']['x'] = False


    # FIXME go through all classes the user is part of, and set the permissions accordingly


    return toret, 200

def can_read(chatroomID: str, channelID: str, username: str):
    """
        This function implements a small speed boost for public channels in contrast with get_channel_permissions when checking if a user can read

        return:
            bool, status
    """

    # get channel info
    channel_obj, status = fetch_channel(chatroomID, channelID)
    if status != 200:
        return channel_obj, status


    # everyone can read from public channels
    if channel_obj['public'] == True:
        return True, 200



    # if above doesnt match then just return whatever the slower function returns
    permissions, status = get_channel_permissions(chatroomID, channelID, username)
    if status != 200:
        return permissions, status

    return permissions['permissions']['r'], 200

def get_readable_channels(chatroomID: str, username: str):
    """
        Gets a list of all channels that are readable

        return:
            [
                {
                    channelID: "UUID",
                    channel_name: "default || something else",
                    public: True/False || 1/0
                }
            ]

    """

    channels, status = fetch_all_channels(chatroomID)
    if status != 200: return channels, status

    new_channels = []
    for channel in channels:
        if can_read(chatroomID, channel['channelID'], username)[0]:
            new_channels.append(channel)

    return new_channels, 200






#-------------------------------------------------------------- Users -----------------------
def write_user(chatroomID: str, username: str, nickname: str, password: str):
    """ write user to database """

    # hash password
    password = security.hashpw(password)


    # get db
    db = database(chatroomID)


    # Check if this is the first user in the chatrtoom.
    # If this is the case then assign the constructor rank to the user
    users, status = db.select("*", "users")
    if status != 200:
        return "Internal database error while checking users", status
    if len(users) < 1:
        db.insert('userclasses', ('0', username))


    # save details of user
    res, status = db.insert('users', (username, nickname, password))
    if status != 200:
        return f"internal database error while saving user credientials.", status


    # set user colour
    res, status = db.insert('colours', (username, None,None,None))
    if status != 200:
        return f"internal database error while setting user colour.", status

    db.commit()
    db.close()
    return "OK", 200

def fetch_user_creds(chatroomID: str, username: str):
    """
        If user exists, fetch all their nickname and password.

    return:
        {
                "username": "0 || UUID",
                "nickname": "string",
                "password": "hash"
                }
    """

    # get db
    db = database(chatroomID)

    # get info on user
    info, status = db.select("*", "users", "username=?", (username,))
    if status != 200:
        return "Internal database error, failed to stat user.", 500


    # check if user exists
    if len(info) < 1:
        return "User does not exist", 404


    # db responds with a tuple
    info = info[0]


    retobj = {
            "username": info[0],
            "nickname": info[1],
            "password": info[2]
            }

    db.close()
    return retobj, 200

def fetch_user(chatroomID: str, username: str):
    """
        Fetch all 'public' data about a user.
        Public data includes all information other than the password or cookies.

        return:
            {
                username: 'string',
                nickname: "string",
                colour: {
                    r: 0,
                    g: 0,
                    b: 0
                    }
            }
    """

    # Re-using functions is neat. :)
    usercreds, status = fetch_user_creds(chatroomID, username)
    if status != 200: usercreds, status


    db = database(chatroomID)

    colours, status = db.select("*", "colours", "username=?", (username,))
    if status != 200:
        return "Internal database error while getting user colours", 500


    try:
        colour = colours[0]

        colour = {
                "r": colour[1],
                "g": colour[2],
                "b": colour[3]
                }

    except Exception as e:
        log.error(fetch_user, f"Error occured while formatting colours: {e}")
        return "Internal server error while formatting colours", 500



    toret = {
            "username": username,
            "nickname": usercreds['nickname'],
            "colour": colour
            }


    db.close()
    return toret, 200





#-------------------------------------------------------------- Cookies -----------------------
def store_cookie(chatroomID: str, username: str, cookie: str):
    """ Writes a cookie to the database """

    db = database(chatroomID)

    status = db.insert('cookies', (username, cookie))[1]
    if status != 200:
        return "Internal database error while setting cookie.", 500


    db.commit()
    db.close()
    return "OK", 200

def get_cookies(chatroomID: str, username: str, cookie: str):
    """ Get all cookies associated with a user. """

    db = database(chatroomID)

    cookies, status = db.select("cookie", "cookies", "username=?", (username,))
    if status != 200:
        return "Internal database error while getting cookies.", 500

    # get rid of useless tuple
    no_tuple_cookies = []
    for i in cookies:
        no_tuple_cookies.append(i[0])

    db.close()
    return no_tuple_cookies, 200




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


