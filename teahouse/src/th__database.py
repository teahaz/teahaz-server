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

import time
import json
import logging
import pymongo
import codectrl

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
        self.exists: bool = chatroom_id in MONGODB.list_database_names()

        self.db_handle = MONGODB[chatroom_id]

        # Variable to keep track of whether the user exists
        # (similar reason to database exits)
        # TODO: replace this with an actual check.
        self.user_exists: bool = False

    def init_chatroom(self, chatroom_name: str):
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
        if self.exists is True:
            logging.error("Attempted to re-create chatroom: %s", self.chatroom_id)
            return {"error": "Will not re-create the chatroom."}, 409


        # There should be no reason for this function
        # to be called without a password and a nickname.
        # If this is the case then some checks were forgotten
        # by the developer.
        if self.password == "" and not isinstance(self.password, str):
            return {
                    "error":
                    "Internal server error: Panicked at missing or wrong password\
                            , this should never happen."
                    }, 500
        if self.nickname == "" and not isinstance(self.nickname, str):
            return {
                    "error":
                    "Internal server error: Panicked at missing or wrong nickname\
                            , this should never happen."
                    }, 500
        if chatroom_name != "" and not isinstance(chatroom_name, str):
            return {
                    "error":
                    "Internal server error: Panicked at missing or wrong chatroom name\
                            , this should never happen."
                    }, 500



        # Create the default user, called the "constructor".
        # This is our internal name for the "super admin",
        # an admin that cannot be removed from the chatroom
        users_collection = self.db_handle.users
        document_constructor_user = {
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
                    "classes": ['0'] # Id of the classes that the user is part of
                                     # Only the constructor has a class_id of 0
                }
            }
        users_collection.insert_one(document_constructor_user)



        # Insert the default classes into the database.
        # The two default classes we have is the "constructor"
        # class and the "default" class.
        # Constructor:
        #   The constructor class is the "super admin" class that is only for the chatroom creator
        # Default:
        #   The default class is a class that all members other than the constructor has to
        #   be part of. It is synonymous with "everyone" in some other messaging applications.
        classes_collection = self.db_handle.classes
        document_constructor_class = {
                "_id": "0",
                "public":
                {
                    "class-id": "0", # only class_id 0 can kick an admin, and 0 cannot be kicked
                    "name": "constructor",
                    "admin": True # if a class is admin then it doesn't need to check permissions
                }
            }
        document_default_class = {
                "_id": "1",
                "public":
                {
                    "class-id": "1",
                    "name": "default",
                    "admin": False
                }
            }
        classes_collection.insert_many([document_constructor_class, document_default_class])


        # Insert the general channel into the database.
        # The chatroom cannot really run without having
        # at least one channel. This general channel is
        # just a channel that is added by the server when
        # the chatroom is created.

        # In settings this will be marked with the
        # "default channel" property. There always
        # has to be a default channel in the server,
        # so any channel marked with this cannot be
        # deleted. However this setting can be changed,
        # so this original channel can be deleted, if
        # a new default channel is elected beforehand.
        channels_collection = self.db_handle.channels
        default_channel_id = security.gen_uuid()
        document_default_channel = {
                "_id": default_channel_id,
                "public":
                {
                    "channel-id": default_channel_id,
                    "name": "default", # maybe make this configurable on the server level
                    "permissions":
                    [
                        {
                            "class-id": "1",
                            "r": True, # read access to the channel
                            "w": True, # "write" or send access
                            "x": False # per-channel admin
                        }
                    ]
                }
            }
        channels_collection.insert_one(document_default_channel)


        # Create a "newuser" event in the default channel
        # to display that the constructor user has joined.
        # This should not by default be a visible message,
        # but is up to the client to decide how they want
        # to display it.
        messages_collection = self.db_handle.messages
        welcome_message_id = security.gen_uuid()
        document_welcome_message = {
                "_id": welcome_message_id,
                "public":
                {
                    "message-id": welcome_message_id,
                    "channel-id": document_default_channel['_id'],
                    "time": time.time(),
                    "type": "system",
                    "data": {
                        "event-type": "newuser",
                        "user-info": document_constructor_user['public']
                        }
                }
            }
        messages_collection.insert_one(document_welcome_message)


        # Insert the default settings. Settings hold values about the
        # chatroom that can be changed by admins or server owners.
        # This include various things like the minimum password length,
        # the default channel or the name of the chatroom.

        # Each setting has 4 values:
        #   - sname is the name of the setting. This can be displayed to users.
        #   - svalue is the value of the setting. This can be changed with right permissions.
        #   - stype is the datatype of the svalue field
        #   - mutable represents whether a chatroom admin can change this.
        #           If false then only a server admin can do so (config files).

        # TODO: create configuration files and fill  these in automatically from them
        settings_collection = self.db_handle.settings
        array_default_settings = [
                {
                    "_id": security.gen_uuid(),
                    "public":
                    {
                        "sname": "Chatroom name",
                        "svalue": str(chatroom_name),
                        "stype": "string",
                        "mutable": True
                    },
                },
                {
                    "_id": security.gen_uuid(),
                    "public":
                    {
                        "sname": "Minimum password length",
                        "svalue": 10,
                        "stype": "int",
                        "mutable": False
                    },
                },
                {
                    "_id": security.gen_uuid(),
                    "public":
                    {
                        "sname": "default_channel", # The channel where system messages get sent
                        "svalue": document_default_channel['_id'],
                        "stype": "UUID[str]",
                        "mutable": True
                    },
                },
            ]
        settings_collection.insert_many(array_default_settings)

        # set state variables for the Database object
        self.exists = True
        self.user_exists = True

        chatroom_details =  {
                "chatroom-id": self.chatroom_id,
                "chatroom-name": chatroom_name,
                "users": [document_constructor_class['public']],
                "channels": [document_default_channel['public']],
                "classes": [document_constructor_class['public'], document_default_class['public']],
                "settings": [x['public'] for x in array_default_settings]
                }

        codectrl.log(json.dumps(chatroom_details, indent=4), status=200)
        return chatroom_details, 200
