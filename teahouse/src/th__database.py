"""

This module exports the database class.
This is an object as an interface that makes working
with the database a lot easier.

In addition it makes sure that the user has rights
to do the functions that they attempted to do, before
executing them.


It is important that access control takes place on the
database level as this way it is harder for a future
developer to forget access-control on a method.

"""

import logging
import codectrl
import pymongo

import th__security as security

# Connect to the mongo-db server.
MONGODB = pymongo.MongoClient('mongodb', 27017)

class Database:
    """
        Database class that handles all database
        operations.

        The class is implemented in a user-centric way
        where each instance can only do things that
        the user that it got initiated with has rights
        to do.
    """
    def __init__(self, chatroom_id: str, username: str, password: str = "", nickname: str = ""):
        """
            The username field is required for the database,
            to comply with the user-centric way access control.

            Furthermore the (optional) password and nickname
            arguments are for users that have not yet registered.
        """

        self.username: str = username
        self.password: str = password
        self.nickname: str = nickname
        self.chatroom_id: str = chatroom_id

        # Variable keeps track of whether the database
        # already exists.
        # This is necessary as mongodb lazy-creates databases.
        # If we reference a database without it existing, it
        # could get created without the needed tables added to it.
        self.exits: bool = chatroom_id in MONGODB.list_database_names()

        self.db_handle = MONGODB[chatroom_id]

        # Variable to keep track of whether the user exists
        # (similar reason to database exits)
        # TODO: replace this with an actual check.
        self.user_exits: bool = False

    def init_chatroom(self):
        """
            Function creates a chatroom database,
            and adds at least one default document into
            each collection.

            This function also needs to add the constructor
            to the chatroom. (The constructor is the name
            we give the "super admin" that created the chatroom.)
            In order to add this user, it needs the password and
            nickname fields.


            Database model:
             Each chat-room has its own database. These databases
             are split into collections for different categories.
             Each collection will have their own documents for
             each element for the collection.

             This means that for example each class within
             the classes collection has its own document.


            Collections:
                - Users    -- Collection of all users.
                - Classes  -- Collection of all user-groups.
                - Channels -- Collection of all channels.
                - Messages -- Collection of all messages.
                - Settings -- Collection of all settings.
                (This last one used to be just one document, now its a collection)

            Default documents:
                - A default user: "Constructor" of the chat-room
                - 2 default classes: "default" and "constructor".
                - A default channel called "default".
                - 3 default settings for chatroom_name, password_length and default_channel.
                - A welcome message in the messages collection.
        """
        # If there is already a database with this name
        if self.exits is True:
            logging.error("Attempted to re-create chatroom: %s", self.chatroom_id)
            return {"error": "Will not re-create the chatroom."}, 409


        # There should be no reason for this function
        # to be called without a password and a nickname.
        # If this is the case then some checks were forgotten
        # by the developer.
        if self.password != "":
            return {
                    "error":
                    "Internal server error: Panicked at missing password, this should never happen."
                    }, 500
        if self.nickname != "":
            return {
                    "error":
                    "Internal server error: Panicked at missing nickname, this should never happen."
                    }, 500




        # Variables starting with document_ represent that
        # the variable holds a single document.
        document_default_user = {
                "_id": str(self.username),
                "private":
                {
                    "password": self.password,
                    "cookies": []
                },
                "public":
                {
                    "username": str(self.username),
                    "nickname": str(self.nickname),
                    "colour":
                    {
                        "r": None,
                        "g": None,
                        "b": None,
                    },
                    "classes": []
                }
            }


        # need to add the other default documents



