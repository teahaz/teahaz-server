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



class login(Resource):
    def post(self, chatroomID): # log into chatrom
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


class chatrooms(Resource):
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


class invites(Resource):
    def get(self, chatroomID):
        if not request.get_json(): return "no data sent", 401
        if not chatroomID: return "ChatroomId was not part of the path", 400
        if not filesystem.chatroom_exists(chatroomID): return "Chatroom does not exist.", 404
        if not users.check_cookie(chatroomID, request.cookies.get(chatroomID), request.headers.get('userID')):
            return "Client not logged in. (cookie or userID was not sent)", 401

        return "OK", 200



restful.add_resource(chatrooms, '/api/v0/chatroom', '/api/v0/chatroom/')
restful.add_resource(login, '/api/v0/login/<chatroomID>', '/api/v0/login/<chatroomID>/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=13337, debug=True)
