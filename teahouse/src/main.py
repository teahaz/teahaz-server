"""
Main module.

This module actually starts the server
and handles incoming requests / responses.
"""


from flask import Flask
from flask import request
from flask import make_response

from flask_restful import Api
from flask_restful import Resource


import api
import users_th as users
import global_helpers as helpers


# setup logging
from logging_th import logger
LOG = logger()


# inisiate flask
app = Flask(__name__)
restful = Api(app)


class Chatrooms(Resource):
    """ /api/v0/chatrooms """
    def post(self, chatroom_id=None): # pylint: disable=no-self-use
        """ Method for creating chatrooms """

        # In this method chatroomID doesnt mean anything,
        # but its best to set it to None anyway just incase
        # some looser sent a chatroomID to create_chatroom.
        chatroom_id = None

        # check data
        res, status = helpers.check_default(
                'post',
                None,
                request,
                False
            )
        if status != 200:
            return res, status


        # create chatroom
        chat_obj, status = api.create_chatroom(request.get_json())

        # creating chatroom failed
        if status != 200:
            return chat_obj, status

        cookie, status = users.set_cookie(chat_obj['chatroomID'], request.get_json()['username'])

        # storing cookie failed
        if status != 200:
            return cookie, status

        # set cookie for user and return
        res = make_response(chat_obj)
        res.set_cookie(chat_obj.get('chatroomID'), cookie)
        return res


    def get(self, chatroom_id=None): # pylint: disable=no-self-use
        """
            Get information about a chatroom,
            also used to check if you are logged in
        """

        # check chatroom_id as this method will work without it too
        if not chatroom_id:
            return "ChatroomID must be included in the path for this method", 400

        # check data
        res, status = helpers.check_default(
                'get',
                chatroom_id,
                request,
                True
            )
        if status != 200:
            return res, status

        return helpers.get_chat_info(chatroom_id, request.headers.get('username'))


class Login(Resource):
    """ /api/v0/login/ """

    def post(self, chatroom_id): # pylint: disable=no-self-use
        """ Login to a chatrom. """

        # check data
        res, status = helpers.check_default(
                'post',
                chatroom_id,
                request,
                False
            )
        if status != 200:
            return res, status


        # auth chatroom
        chatroom_data, status = api.login(chatroom_id, request.get_json())
        if status != 200:
            return chatroom_data, status



        # set cookie
        cookie, status = users.set_cookie(chatroom_id, request.get_json()['username'])
        if status != 200:
            return cookie, status


        # return with cookie
        res = make_response(chatroom_data)
        res.set_cookie(chatroom_id, cookie)
        return res


class Channels(Resource):
    """ /api/v0/channels/ """
    def post(self, chatroom_id): # pylint: disable=no-self-use
        """ Creating a new channel """

        # check data
        res, status = helpers.check_default(
                'post',
                chatroom_id,
                request,
                True
            )
        if status != 200:
            return res, status

        return api.create_channel(chatroom_id, request.get_json())


class Messages(Resource):
    """ /api/v0/messages/ """

    def post(self, chatroom_id): # pylint: disable=no-self-use
        """ send message to server """

        # check data
        res, status = helpers.check_default(
                'post',
                chatroom_id,
                request,
                True
            )
        if status != 200:
            return res, status

        return api.send_message(chatroom_id, request.get_json())

    def get(self, chatroom_id): # pylint: disable=no-self-use
        """ Get a message """

        # check data
        res, status = helpers.check_default(
                'get',
                chatroom_id,
                request,
                True
            )
        if status != 200:
            return res, status

        return api.get_messages(chatroom_id, request.headers)


class Invites(Resource):
    """ /api/v0/invites/ """

    def post(self, chatroom_id): # pylint: disable=no-self-use
        """ Join a chatroom by invite """

        # check data
        res, status = helpers.check_default(
                'post',
                chatroom_id,
                request,
                False
            )
        if status != 200:
            return res, status


        # check and use invite
        chatroom_data, status = api.use_invite(chatroom_id, request.get_json())
        if status != 200:
            return chatroom_data, status


        # set cookie
        cookie, status = users.set_cookie(chatroom_id, request.get_json()['username'])
        if status != 200:
            return cookie, status


        # return with cookie
        res = make_response(chatroom_data)
        res.set_cookie(chatroom_id, cookie)
        return res



    def get(self, chatroom_id): # pylint: disable=no-self-use
        """ Create a new invite to a chatroom """

        # check data
        res, status = helpers.check_default(
                'get',
                chatroom_id,
                request,
                True
            )
        if status != 200:
            return res, status

        return api.create_invite(chatroom_id, request.headers)



# NOTE could add to invites a /api/v0/invite/chatroomID/inviteID,
#   which could just return data about an invite without needing
#   for auth or anything

restful.add_resource(Chatrooms,
        '/api/v0/chatroom',
        '/api/v0/chatroom/',
        '/api/v0/chatroom/<chatroom_id>',
        '/api/v0/chatroom/<chatroom_id>/')
restful.add_resource(Login,    '/api/v0/login/<chatroom_id>',    '/api/v0/login/<chatroom_id>/')
restful.add_resource(Invites,  '/api/v0/invites/<chatroom_id>',  '/api/v0/invites/<chatroom_id>/')
restful.add_resource(Channels, '/api/v0/channels/<chatroom_id>', '/api/v0/channels/<chatroom_id>/')
restful.add_resource(Messages, '/api/v0/messages/<chatroom_id>', '/api/v0/messages/<chatroom_id>/')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=13337, debug=True)
