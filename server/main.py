from os import environ

from flask import Flask
from flask import request
from flask import redirect
from flask import make_response
from flask import render_template

from flask_restful import Api
from flask_restful import Resource

from api import upload_file
from api import message_get
from api import message_send
from api import download_file

from users_th import add_user
from users_th import set_cookie
from users_th import check_cookie

from dbhandler import check_databses

from logging_th import logger as log

app = Flask(__name__)
api = Api(app)

# request size limit, not to overload server memory
#this should never be bigger then the amount of ram the server has
app.config['MAX_CONTENT_LENGTH'] = 1000000000 # one gb,



class index(Resource):
    def get(self):
        return render_template("index.html")



class register(Resource):
    def post(self):
        if not request.get_json(): return "no data sent", 401
        response, status_code = add_user(request.get_json())
        return response, status_code



# checks password and returns auth cookie for use in other places
class login(Resource):
    def post(self):
        if not request.get_json(): return "no data sent", 401
        # authenticate and get cookie data
        cookie, status_code = set_cookie(request.get_json())

        # using 200 and not True bc it gets sent along to the client
        if status_code == 200:
            # set cookie
            res = make_response("assigning new cookie")
            res.set_cookie('access', cookie)
            return res
        else:
            # if the cookie fails to set then this is not actaully a cookie but an error message
            return cookie, status_code

    def get(self):
        if not request.headers: return "no data sent", 401
        if not check_cookie(request.cookies.get('access'), request.headers): return "client not logged in", 401
        return "OK", 200


# handles messages
class api__messages(Resource):
    def get(self): # gets messages since {time.time()}
        if not request.headers: return "no data sent", 401
        if not check_cookie(request.cookies.get('access'), request.headers): return "client not logged in", 401

        data, status_code = message_get(request.headers)
        return data, status_code


    def post(self): # sends message
        if not request.get_json(): return "no data sent", 401
        if not check_cookie(request.cookies.get('access'), request.get_json()): return "client not logged in", 401

        data, status_code = message_send(request.get_json())
        return data, status_code



# handles file
class api__files(Resource):
    def get(self): #gets file
        if not request.headers: return "no data sent", 401
        if not check_cookie(request.cookies.get('access'), request.headers): return "client not logged in", 401

        data, status_code = download_file(request.headers)
        return data, status_code


    def post(self): # sends file
        if not request.get_json(): return "no data sent", 401
        if not check_cookie(request.cookies.get('access'), request.get_json()): return "client not logged in", 401

        data, status_code = upload_file(request.get_json())
        return data, status_code



#legend
api.add_resource(index, '/')
api.add_resource(login, '/login')
api.add_resource(register, '/register')
api.add_resource(api__files, '/api/v0/file/')
api.add_resource(api__messages, '/api/v0/message/')



if __name__ == "__main__":
    ## start the server in debug mode
    response, status_code = check_databses()
    if status_code != 200:
        log(level='fail', msg=f"[main] fatal erorr with databasess\nTraceback: {response}")
        import sys
        sys.exit(-1)

    app.run(host='0.0.0.0', port=13337, debug=True)
