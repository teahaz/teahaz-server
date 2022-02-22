"""
Main module of the teahaz-server.

This module starts the server, handles
incoming requests and returns responses.
"""


from flask import Flask
from flask import request
from flask import make_response

from flask_restful import Api
from flask_restful import Resource


# Logging
#
# The server has 2 types of logging.
#
# First it uses codectrl for debugging.
# These are very detailed logs that only
# trigger when the environment variable
# CODECTRL_DEBUG is set to a truthy value.
# This cannot be always on as it is very cpu
# intensive and needs the codectrl application
# to be running.
#
# Secondly it uses the colouredlogs library.
# This is library is used for standard,
# informational logs. Some of these will be
# included in production builds too.
import codectrl
import coloredlogs


# Initialise flask and flask_restful objects.
app_regular = Flask(__name__)
app_restful = Api(app_regular)



class Chatrooms(Resource):
    """ /api/v0/chatroom/ """
    def post(self, chatroom_id=None): # pylint: disable=no-self-use
        """ Method for creating chat-rooms """
        codectrl.log("method: Create chat-room", chatroom_id=chatroom_id)


    def get(self, chatroom_id=None): # pylint: disable=no-self-use
        """
            Method for getting information about a chat-room.
            Can also be used to check whether your cookies are valid.
        """
        codectrl.log("Method: get chat-room", chatroom_id=chatroom_id)


class Login(Resource):
    """ /api/v0/login/ """
    def post(self, chatroom_id): # pylint: disable=no-self-use
        """ Method to log in (get cookies) to a chat-room """
        codectrl.log("Method: login", chatroom_id=chatroom_id)


class Channels(Resource):
    """ /api/v0/channels/ """
    def post(self, chatroom_id): # pylint: disable=no-self-use
        """ Method to create a new channel """
        codectrl.log("Method: create channel", chatroom_id=chatroom_id)


class Messages(Resource):
    """ /api/v0/messages/ """

    def post(self, chatroom_id): # pylint: disable=no-self-use
        """ Method to send a message """
        codectrl.log("Method: send message", chatroom_id=chatroom_id)

    def get(self, chatroom_id): # pylint: disable=no-self-use
        """ Method to get messages """
        codectrl.log("Method: get message", chatroom_id=chatroom_id)


class Invites(Resource):
    """ /api/v0/invites/ """

    def post(self, chatroom_id): # pylint: disable=no-self-use
        """ Method to join a chat-room with an invite. """
        codectrl.log("Method: use invite", chatroom_id=chatroom_id)


    def get(self, chatroom_id): # pylint: disable=no-self-use
        """ Method to create a new invite """
        codectrl.log("Method: create invite", chatroom_id=chatroom_id)




# Defined paths
#
# Below are all the path's that exist
# on the server.
#
# Each method has to be defined with and
# without the trailing slash, otherwise
# it will not be recognised in both circumstances.
#
# Furthermore the chatroom method has to be
# defined 4 times to include methds when
# the chatroom_id is not present.
# (at the creation of the chat-room)
app_restful.add_resource(Chatrooms,
            '/api/v0/chatroom',
            '/api/v0/chatroom/',
            '/api/v0/chatroom/<chatroom_id>',
            '/api/v0/chatroom/<chatroom_id>/')
app_restful.add_resource(Login,
            '/api/v0/login/<chatroom_id>',
            '/api/v0/login/<chatroom_id>/')
app_restful.add_resource(Invites,
            '/api/v0/invites/<chatroom_id>',
            '/api/v0/invites/<chatroom_id>/')
app_restful.add_resource(Channels,
            '/api/v0/channels/<chatroom_id>',
            '/api/v0/channels/<chatroom_id>/')
app_restful.add_resource(Messages,
            '/api/v0/messages/<chatroom_id>',
            '/api/v0/messages/<chatroom_id>/')


# When running locally the app is run
# with debug mode on and all hosts accepted.

# When deployed this does not get run as
# under gunicorn  __name__ is not equal
# to __main__.
if __name__ == "__main__":
    coloredlogs.install()
    app_regular.run(host="0.0.0.0", port=13337, debug=True)
