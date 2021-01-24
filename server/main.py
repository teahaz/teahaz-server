from os import environ

from flask import Flask, render_template, request, make_response
from flask_restful import Resource, Api


from api import message_send
from api import message_get
from api import upload_file
from api import download_file

from users_th import set_cookie


app = Flask(__name__)
api = Api(app)

# request size limit, not to overload server memory
#this should never be bigger then the amount of ram the server has
app.config['MAX_CONTENT_LENGTH'] = 1000000000 # one gb,


class index(Resource):
    def get(self):
        return render_template("index.html")


# checks password and returns auth cookie for use in other places
class login(Resource):
    def post(self):
        cookie = set_cookie(request.get_json())
        res = make_response("assigning new cookie")
        res.set_cookie('token', cookie, max_age=60*60*24*100) # cookie age is rn 100 days, i will research what is best for this later
        return res, 200


# handles messages
class api__messages(Resource):
    # gets messages since {time.time()}
    def get(self):
        data, response = message_get(request.headers)
        return data, response
    # sends message
    def post(self):
        data, response = message_send(request.get_json())
        return data, response


# handles file
class api__files(Resource):
    #gets file
    def get(self):
        data, response = download_file(request.headers)
        return data, response
    # sends file
    def post(self):
        data, response = upload_file(request.get_json())
        return data, response



api.add_resource(index, '/')
api.add_resource(login, '/login')
api.add_resource(api__files, '/api/v0/file/')
api.add_resource(api__messages, '/api/v0/message/')



if __name__ == "__main__":
    ## start the server, in debug mode
    app.run(host='localhost', port=5000, debug=True)
