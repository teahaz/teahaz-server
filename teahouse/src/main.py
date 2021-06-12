from os import environ

from flask import Flask
from flask import request
from flask import make_response

from flask_restful import Api
from flask_restful import Resource


import api
# import users_th as users
# import dbhandler as database
# import security_th as security
# import filesystem_th as filesystem


# setup logging
from logging_th import logger
global log
log = logger()


# inisiate flask
app = Flask(__name__)
restful = Api(app)



class chatrooms(Resource):
    def post(self): # create chatroom
        if not request.get_json(): return "no data sent", 401

        # create chatroom
        chat_obj, status = api.create_chatroom(request.get_json())

        # If creating chatroom worked then log set the users cookie
        # so that they are automatically logged in.
        if status == 200:
            cookie, status = users.set_cookie(request.get_json(), chat_obj.get('chatroom'))

            # make successful response
            if status == 200:
                res = make_response(chat_obj)
                res.set_cookie(dict(chat_obj).get('chatroom'), cookie)
                return res

            # failed to set cookie
            else:
                return cookie, status

        # creating chatroom failed
        return chat_obj, status




restful.add_resource(chatrooms, '/api/v0/chatroom', '/api/v0/chatroom/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=13337, debug=True)
