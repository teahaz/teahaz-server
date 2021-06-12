import os
import sqlite3

import security_th as security

# setup logging
from logging_th import logger
global log
log = logger()




class database():
    """ Abstraction over database functions """
    def __init__(self, chatroomID: str):
        if not os.path.exists('storage/chatrooms/{chatroomID}'):
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
            log.error(self, "Database operation failed: {e}")
            return f"Database operation failed: {e}", 500


    def close(self):
        """
            Close database.

            This method MUST be run after using the database
        """
        self.db.close()


    def create(self, table: str, values: list):
        """ Wrapper around creating tables """

        values = str(values).strip('[').strip(']')
        statement = f"CREATE TABLE {table} ({values})"

        cursor, status= self._run(statement)

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


    def insert(self, table: str, values: list):
        """ Wrapper around adding data to the database """

        # Get (?, ?, ?) like syntax
        rowcount = len(values)
        row = "(" + ("?, "*rowcount).strip(', ') + ")"

        # run
        statement = f"INSERT INTO {table} VALUES {row}"
        return self._run(statement, encoded_values)












def init_chat(chatroomID: str, chat_name: str):
    """ Create chatroom database and add tables """
    log.log(init_chat, "Creating chatroom {chatroomID}")

    # Get db object
    db = database(chatroomID)
    if not db.exists:
        return f"Chatroom: {chatroomID}, does not exist!", 404


    # add tables
    db.create('settings',    ['sname',   'svalue'])
    db.create('invites',     ['inviteID', 'userID', 'classID', 'bestbefore', 'uses'])

    db.create('users',       ['userID',  'username', 'password'])
    db.create('colours',     ['userID',  'r', 'g', 'b'])
    db.create('cookies',     ['userID',  'cookie'])

    db.create('classes',     ['classID', 'classname'])
    db.create('userclasses', ['classID', 'userID'])

    db.create('channels',    ['channelID', 'channelname',  'public'])
    db.create('permissions', ['channelID', 'classID', 'r', 'w', 'x'])

    db.create('messages',    ['messageID', 'channelID', 'userID', 'replyID', 'type', 'data'])
    db.create('files',       ['fileID', 'filename', 'size'])


    # Add chat_name to settings
    status = db.insert('settings', ['chat_name', chat_name])[1]
    if status != 200:
        return "Failed to crete chatroom. Error while setting chat_name.", 500


    # Add 'default' to channels
    status = db.insert('channels', [security.gen_uuid(), 'default', True])
    if status != 200:
        return "Failed to crete chatroom. Error while creating default chatroom.", 500


    # Add 'admin' class
    status = db.insert('classes', [security.gen_uuid(), 'admin'])
    if status != 200:
        return "Failed to crete chatroom. Error while creating 'admin' class.", 500


    return "OK", 200










