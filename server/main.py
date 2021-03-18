from os import environ

from flask import Flask
from flask import request
from flask import redirect
from flask import make_response
from flask import render_template

from flask_restful import Api
from flask_restful import Resource

#from api import upload_file
from api import message_get
from api import message_send
#from api import download_file
from api import create_invite
from api import create_chatroom

from users_th import process_invite
from users_th import add_user
from users_th import set_cookie
from users_th import check_cookie

from dbhandler import check_settings
from dbhandler import check_databses

from logging_th import logger as log

app = Flask(__name__)
api = Api(app)

# request size limit, not to overload server memory
#this should never be bigger then the amount of ram the server has
app.config['MAX_CONTENT_LENGTH'] = 1000000000 # one gb,



class index(Resource):
    def get(self):
        # return render_template("index.html")
        return redirect('https://github.com/tHoMaStHeThErMoNuClEaRbOmB/teahaz-server')




# checks password and returns auth cookie for use in other places
class login(Resource):
    def post(self, chatroomId):
        if not request.get_json(): return "[main/login/0] || no data sent", 401
        if not chatroomId: return "[main/login/1] || ChatroomId was not part of the path", 401

        # authenticate and get cookie data
        cookie, status_code = set_cookie(request.get_json(), chatroomId)


        # NOTE : this is temporary
        # TODO all these endpoints get the chatname in a different way. TODO: make it more uniform
        chat_name, status_code = check_settings(chatroomId, "chatroom_name")
        if status_code != 200:
            return chat_name, status_code
        # NOTE : this is temporary ^^

        # using 200 and not True bc it gets sent along to the client
        if status_code == 200:
            # set cookie
            res = make_response({"name": chat_name, "chatroom": chatroomId})
            res.set_cookie(chatroomId, cookie)
            return res

        else:
            # if the cookie fails to set then this is not actaully a cookie but an error message
            return cookie, status_code

    def get(self, chatroomId):
        if not request.headers: return "no data sent", 401
        if not check_cookie(request.cookies.get(chatroomId), request.headers, chatroomId): return "client not logged in", 401
        return "OK", 200



# handles messages
class api__messages(Resource):
    def get(self, chatroomId): # gets messages since {time.time()}
        if not request.headers: return "no data sent", 401
        if not check_cookie(request.cookies.get(chatroomId), request.headers, chatroomId): return "client not logged in", 401

        data, status_code = message_get(request.headers, chatroomId)
        return data, status_code


    def post(self, chatroomId): # sends message
        if not request.get_json(): return "no data sent", 401
        if not check_cookie(request.cookies.get(chatroomId), request.get_json(), chatroomId): return "client not logged in", 401

        data, status_code = message_send(request.get_json(), chatroomId)
        return data, status_code


#
## handles file
#class api__files(Resource):
#    def get(self): #gets file
#        if not request.headers: return "no data sent", 401
#        if not check_cookie(request.cookies.get('access'), request.headers): return "client not logged in", 401
#
#        data, status_code = download_file(request.headers)
#        return data, status_code
#
#
#    def post(self): # sends file
#        if not request.get_json(): return "no data sent", 401
#        if not check_cookie(request.cookies.get('access'), request.get_json()): return "client not logged in", 401
#
#        data, status_code = upload_file(request.get_json())
#        return data, status_code
#
#
#
class api__chatroom(Resource):
    def post(self): # create chatroom
        if not request.get_json(): return "[main/chatroom/0] || no data sent", 401

        # create chatroom
        chat_obj, status_code = create_chatroom(request.get_json())

        # if success, set cookie
        if status_code == 200:
            cookie, status_code = set_cookie(request.get_json(), chat_obj.get('chatroom'))

            if status_code == 200:
                # make response and send cookie
                res = make_response(chat_obj)
                res.set_cookie(dict(chat_obj).get('chatroom'), cookie)
                return res

            else:
                return cookie, status_code


        return chat_obj, status_code





class api__invites(Resource):
    def get(self, chatroomId):
        if not request.headers: return "[main/invites/get/0] || no data sent", 401
        if not chatroomId: return "[main/invites/get/1] || ChatroomId was not part of the path", 401
        if not check_cookie(request.cookies.get(chatroomId), request.headers, chatroomId): return "[main/invites/2] || client not logged in", 401

        response, status_code = create_invite(request.headers, chatroomId)
        return response, status_code


    def post(self, chatroomId):
        if not request.headers: return "[main/invites/post/0] || no data sent", 401
        if not chatroomId: return "[main/invites/post/1] || ChatroomId was not part of the path", 401

        #process invite
        chat_obj, status_code = process_invite(request.get_json(), chatroomId)

        # if success set cookie
        if status_code == 200:
            cookie, status_code = set_cookie(request.get_json(), chat_obj.get('chatroom'))

            if status_code == 200:
                # make response and send cookie
                res = make_response(chat_obj)
                res.set_cookie(dict(chat_obj).get('chatroom'), cookie)
                return res

            else:
                return cookie, status_code

        return chat_obj, status_code



#legend
api.add_resource(index, '/')



api.add_resource(login, '/login/<chatroomId>', '/login/<chatroomId>')
api.add_resource(api__chatroom, '/api/v0/chatroom/', '/api/v0/chatroom/')
#api.add_resource(api__files, '/api/v0/file/<chatroomId>', '/api/v0/file/<chatroomId>')
api.add_resource(api__invites, '/api/v0/invite/<chatroomId>', '/api/v0/invite/<chatroomId>/')
api.add_resource(api__messages, '/api/v0/message/<chatroomId>', '/api/v0/message/<chatroomId>/')



# in dev environment the server is not run as __main__ but this should still run
def check_health():
    response, status_code = check_databses()
    if status_code != 200:
        log(level='fail', msg=f"[health check] ||  fatal erorr with databasess\nTraceback: {response}")
        import sys
        sys.exit(-1)


    # get port for server
    server_port = environ.get('TEAHAZ_PORT')
    print('server_port: ',server_port , type(server_port))
    if not server_port or server_port.isdigit() == False or int(server_port) > 655234 or int(server_port) < 1:
        log(level='log', msg=f"[setup] || TEAHAZ_PORT variable was not set, or is set to an invalid port. Defaulting to '13337'")
        server_port = 13337
    return server_port



server_port = check_health()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=server_port, debug=True)

