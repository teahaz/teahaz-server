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
global log
log = logger()


# inisiate flask
app = Flask(__name__)
restful = Api(app)



class Login(Resource):
    """ /api/v0/login/ """

    def post(self, chatroomID):
        """ Login to a chatrom. """

        # check data
        res, status = helpers.check_default(
                'post',
                chatroomID,
                request,
                False
            )
        if status != 200: return res, status

        # auth chatroom
        chat_obj, status = api.login(chatroomID, request.get_json())
        if status != 200:
            return chat_obj, status

        # set cookie
        cookie, status = users.set_cookie(chatroomID, chat_obj.get('userID'))
        if status != 200:
            return cookie, status

        # return with cookie
        res = make_response(chat_obj)
        res.set_cookie(chatroomID, cookie)
        return res


    def get(self, chatroomID):
        """ Check if you are logged into a chatroom """

        # check data
        res, status = helpers.check_default(
                'get',
                chatroomID,
                request,
                True
            )
        if status != 200: return res, status


        return "Already logged in", 200


class Chatrooms(Resource):
    """ /api/v0/chatrooms """
    def post(self): # create chatroom

        # check data
        res, status = helpers.check_default(
                'post',
                None,
                request,
                False
            )
        if status != 200: return res, status


        # create chatroom
        chat_obj, status = api.create_chatroom(request.get_json())

        # creating chatroom failed
        if status != 200:
            return chat_obj, status

        cookie, status = users.set_cookie(chat_obj.get('chatroomID'), chat_obj.get('userID'))

        # storing cookie failed
        if status != 200:
            return cookie, status

        # set cookie for user and return
        res = make_response(chat_obj)
        res.set_cookie(chat_obj.get('chatroomID'), cookie)
        return res


class Invites(Resource):
    """ /api/v0/invites/ """

    def post(self, chatroomID):
        """ Join a chatroom by invite """

        # check data
        res, status = helpers.check_default(
                'post',
                chatroomID,
                request,
                False
            )
        if status != 200: return res, status

        return api.use_invite(chatroomID, request.get_json())


    def get(self, chatroomID):
        """ Create a new invite to a chatroom """

        # check data
        res, status = helpers.check_default(
                'get',
                chatroomID,
                request,
                True
            )
        if status != 200: return res, status


        return api.create_invite(chatroomID, request.headers)


class Channels(Resource):
    """ /api/v0/channels/ """
    def get(self, chatroomID):
        """ Get details about all channels that the user can read """

        # check data
        res, status = helpers.check_default(
                'get',
                chatroomID,
                request,
                True
            )
        if status != 200: return res, status


        return api.get_channels(chatroomID, request.headers)

    def post(self, chatroomID):
        """ Creating a new channel """

        # check data
        res, status = helpers.check_default(
                'post',
                chatroomID,
                request,
                True
            )
        if status != 200: return res, status

        return api.create_channel(chatroomID, request.get_json())


class Messages(Resource):
    """ /api/v0/messages/ """

    def post(self, chatroomID):
        """ send message to server """

        # check data
        res, status = helpers.check_default(
                'post',
                chatroomID,
                request,
                True
            )
        if status != 200: return res, status

        return api.send_message(chatroomID, request.get_json())

    def get(self, chatroomID):
        """ Get a message """

        # check data
        res, status = helpers.check_default(
                'get',
                chatroomID,
                request,
                True
            )
        if status != 200: return res, status

        return api.get_messages(chatroomID, request.headers)


class Users(Resource):
    """ /api/v0/users/ """

    def get(self, chatroomID):
        """ Get all users of the chatroom """

        # check data
        res, status = helpers.check_default(
                'get',
                chatroomID,
                request,
                True
            )
        if status != 200: return res, status

        return api.get_users(chatroomID, request.headers)





# NOTE could add to invites a /api/v0/invite/chatroomID/inviteID,
#   which could just return data about an invite without needing
#   for auth or anything

restful.add_resource(Chatrooms,'/api/v0/chatroom',              '/api/v0/chatroom/')
restful.add_resource(Login,    '/api/v0/login/<chatroomID>',    '/api/v0/login/<chatroomID>/')
restful.add_resource(Users,    '/api/v0/users/<chatroomID>',    '/api/v0/users/<chatroomID>/')
restful.add_resource(Invites,  '/api/v0/invites/<chatroomID>',  '/api/v0/invites/<chatroomID>/')
restful.add_resource(Channels, '/api/v0/channels/<chatroomID>', '/api/v0/channels/<chatroomID>/')
restful.add_resource(Messages, '/api/v0/messages/<chatroomID>', '/api/v0/messages/<chatroomID>/')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=13337, debug=True)
