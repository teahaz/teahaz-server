import os
import time
import sqlite3

import security_th as security

# setup logging
from logging_th import logger
global log
log = logger()




class database():
    """ Abstraction over database functions """
    def __init__(self, chatroomID: str):

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







def init_chat(chatroomID: str, chat_name: str):
    """ Create chatroom database and add tables """
    log.log(init_chat, f"Creating chatroom {chatroomID}")

    # Get db object
    db = database(chatroomID)
    if not db.exists:
        return f"Chatroom: {chatroomID}, does not exist!", 404


    # add tables
    db.create('settings',    ['sname',   'svalue', 'stype'])
    db.create('invites',     ['inviteID', 'userID', 'classID', 'bestbefore', 'uses'])

    db.create('users',       ['userID',  'username', 'password'])
    db.create('colours',     ['userID',  'r', 'g', 'b'])
    db.create('cookies',     ['userID',  'cookie'])

    db.create('classes',     ['classID', 'classname'])
    db.create('userclasses', ['classID', 'userID'])

    db.create('channels',    ['channelID', 'channelname',  'public'])
    db.create('permissions', ['channelID', 'classID', 'r', 'w', 'x'])

    db.create('messages',    ['messageID', 'channelID', 'userID', 'replyID', 'mtime', 'mtype', 'data'])
    db.create('files',       ['fileID', 'filename', 'size'])


    # Add 'default' to channels
    channelID = security.gen_uuid()
    assert(db.insert('channels', (channelID, 'default', True))[1] == 200)

    # Add default settings
    assert(db.insert('settings', ('chat_name', chat_name, "str"))[1] == 200)
    assert(db.insert('settings', ('min_password_length', 10, "int"))[1] == 200)

    db.commit()
    db.close()
    return channelID, 200



def check_settings(chatroomID: str, setting_name: str):
    """ From settings table fetch setting value corresponding to supplied setting name """

    db = database(chatroomID)

    data, status = db.select('svalue', 'settings', 'sname=?', (setting_name,))
    if status != 200:
        return data, status

    if len(data) < 1:
        return f"Setting '{setting_name}' does not exist!", 404


    db.close()
    return data[0][0], 200



def fetch_user(chatroomID, userID):
    """ Fetch all stored data on a specific user """

    # get db
    db = database(chatroomID)

    # get info on user
    info, status = db.select("*", "users", "True")
    if status != 200:
        return "Internal database error, failed to stat user.", 500

    # db responds with a tuple
    info = info[0]

    retobj = {
            "userID": info[0],
            "username": info[1],
            "password": info[2]
            }

    return retobj, 200




def write_user(chatroomID: str, username: str, password: str):
    """ write user to database """

    # hash password
    password = security.hashpw(password)


    # get db
    db = database(chatroomID)


    # Check if there are any other users already in the chatroom.
    # If this is the first user then they get uid 0,
    # else they get a randomly generated uuid
    users, status = db.select("*", "users", "True")
    if status != 200:
        log.error(write_user, f"Internal database error while checking users: {users}")
        return "Internal database error while checking users", status


    # assign userID
    if len(users) < 1:
        userID = "0"
    else:
        userID = security.gen_uuid()


    # save details of user
    res, status = db.insert('users', (userID, username, password))
    if status != 200:
        log.warn(write_user, f"Failed to add user to database:\n {res}\n\n{userID=}\n{username=}\n{password=}")
        return f"Internal database error while saving user credientials.", status


    db.commit()
    db.close()
    return userID, 200



def write_message(chatroomID: str, channelID: str, userID: str, replyID: str, mtype: str, data: str):
    """ Write message into the messages table """

    # get db
    db = database(chatroomID)

    # get id and time
    mtime = time.time()
    messageID = security.gen_uuid()


    # write message
    status = db.insert("messages", (messageID, channelID, userID, replyID, mtime, mtype, data))[1]
    if status != 200:
        return "Failed to write message.", 500

    db.commit()
    db.close()
    return messageID, 200






def store_cookie(chatroomID: str, userID: str, cookie: str):
    """ Writes a cookie to the database """

    db = database(chatroomID)

    status = db.insert('cookies', (userID, cookie))[1]
    if status != 200:
        return "Internal database error while setting cookie.", 500


    db.commit()
    db.close()
    return "OK", 200


def get_cookies(chatroomID: str, userID: str, cookie: str):
    """ Get all cookies associated with a user. """

    db = database(chatroomID)

    cookies, status = db.select("cookie", "cookies", "userID=?", (userID,))
    if status != 200:
        return "Internal database error while getting cookies.", 500

    # get rid of useless tuple
    cookies = cookies[0]

    return cookies, 200


