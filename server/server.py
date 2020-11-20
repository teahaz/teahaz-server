from flask import Flask, render_template, request
from flask_restful import Resource, Api


from api import message_send
from api import message_get
from api import upload_file
from api import download_file



app = Flask(__name__)
api = Api(app)


class index(Resource):
    def get(self):
        return render_template("index.html")


# handles messages
class api__messages(Resource):
    # gets messages since {time.time()}
    def get(self):
        response, data = message_get(request.get_json())
        return data, response
    # sends message
    def post(self):
        response, data = message_send(request.get_json())
        return data, response


# handles file
class api__files(Resource):
    #gets file
    def get(self):
        response, data = download_file(request.get_json())
        return data, response
    # sends file
    def post(self):
        response, data = upload_file(request.get_json())
        return data, response



api.add_resource(index, '/')
api.add_resource(api__messages, '/api/v0/message/')
api.add_resource(api__files, '/api/v0/file/')


if __name__ == "__main__":
    # these are just set for testing
    app.run(host='localhost', port=5000, debug=True)
