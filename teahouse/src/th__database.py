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

import pymongo

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
    def __init__(self, chatroom_id: str, username: str):
        self.username: str = username
        self.chatroom_id: str = chatroom_id

        # Variable keeps track of whether the database
        # already exists.
        # This is necessary as mongodb lazy-creates databases.
        # If we reference a database without it existing, it
        # could get created without the needed tables added to it.
        self.exits: bool = chatroom_id in MONGODB.list_database_names()

    def init_chatroom(self):
        """
            Function creates a chat-room database,
            and adds at least one default document into
            each collection.


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
