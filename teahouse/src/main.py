from flask import Flask
from flask import request
from flask import make_response

from flask_restful import Api
from flask_restful import Resource


import api
import users_th as users

# import dbhandler as database
import security_th as security
import filesystem_th as filesystem


# setup logging
from logging_th import logger
global log
log = logger()


# inisiate flask
app = Flask(__name__)
restful = Api(app)



class Login(Resource):
    def post(self, chatroomID):
        """ Login to a chatrom. """
        if not request.get_json(): return "no data sent", 401
        if not chatroomID: return "ChatroomId was not part of the path", 400
        if not filesystem.chatroom_exists(chatroomID): return "Chatroom does not exist.", 404

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

        if not chatroomID: return "ChatroomId was not part of the path", 400
        if not filesystem.chatroom_exists(chatroomID): return "Chatroom does not exist.", 404

        if not users.check_cookie(chatroomID, request.cookies.get(chatroomID), request.headers.get('userID')):
            return "Client not logged in. (Cookie or userID was invalid, or not sent)", 401

        return "Already logged in", 200


class Chatrooms(Resource):
    def post(self): # create chatroom
        if not request.get_json(): return "no data sent", 401

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


class Channels(Resource):
    def get(self, chatroomID):
        """ Get details about all channels that the user can read """
        if not request.headers: return "no data sent", 401
        if not chatroomID: return "ChatroomId was not part of the path", 400
        if not filesystem.chatroom_exists(chatroomID): return "Chatroom does not exist.", 404

        if not users.check_cookie(chatroomID, request.cookies.get(chatroomID), request.headers.get('userID')):
            return "Client not logged in. (Cookie or userID was invalid, or not sent)", 401

        return api.get_channels(chatroomID, request.headers)

    def post(self, chatroomID):
        """ Creating a new channel """
        if not request.get_json(): return "no data sent", 401
        if not chatroomID: return "ChatroomId was not part of the path", 400
        if not filesystem.chatroom_exists(chatroomID): return "Chatroom does not exist.", 404

        if not users.check_cookie(chatroomID, request.cookies.get(chatroomID), request.get_json().get('userID')):
            return "Client not logged in. (Cookie or userID was invalid, or not sent)", 401

        return api.create_channel(chatroomID, request.get_json())


class Messages(Resource):
    def post(self, chatroomID):
        """ send message to server """
        if not request.get_json(): return "no data sent", 401
        if not chatroomID: return "ChatroomId was not part of the path", 400
        if not filesystem.chatroom_exists(chatroomID): return "Chatroom does not exist.", 404

        if not users.check_cookie(chatroomID, request.cookies.get(chatroomID), request.get_json().get('userID')):
            return "Client not logged in. (Cookie or userID was invalid, or not sent)", 401

        return api.send_message(chatroomID, request.get_json())

    def get(self, chatroomID):
        """ Get a message """
        if not request.headers: return "no data sent", 401
        if not chatroomID: return "ChatroomId was not part of the path", 400
        if not filesystem.chatroom_exists(chatroomID): return "Chatroom does not exist.", 404

        if not users.check_cookie(chatroomID, request.cookies.get(chatroomID), request.headers.get('userID')):
            return "Client not logged in. (Cookie or userID was invalid, or not sent)", 401

        return api.get_messages(chatroomID, request.headers)


class Users(Resource):
    def get(self, chatroomID):
        """ Get all users of the chatroom """
        if not request.headers: return "no data sent", 401
        if not chatroomID: return "ChatroomId was not part of the path", 400
        if not filesystem.chatroom_exists(chatroomID): return "Chatroom does not exist.", 404

        if not users.check_cookie(chatroomID, request.cookies.get(chatroomID), request.headers.get('userID')):
            return "Client not logged in. (Cookie or userID was invalid, or not sent)", 401

        return api.get_users(chatroomID, request.headers)


restful.add_resource(Chatrooms,'/api/v0/chatroom',              '/api/v0/chatroom/')
restful.add_resource(Login,    '/api/v0/login/<chatroomID>',    '/api/v0/login/<chatroomID>/')
restful.add_resource(Users,    '/api/v0/users/<chatroomID>',    '/api/v0/users/<chatroomID>/')
restful.add_resource(Channels, '/api/v0/channels/<chatroomID>', '/api/v0/channels/<chatroomID>/')
restful.add_resource(Messages, '/api/v0/messages/<chatroomID>', '/api/v0/messages/<chatroomID>/')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=13337, debug=True)
