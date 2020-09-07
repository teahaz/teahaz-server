from flask import Flask, render_template, request
from flask_restful import Resource, Api


from api import message_send
from api import message_get


app = Flask(__name__)
api = Api(app)


class index(Resource):
    def get(self):
        return render_template("index.html")


# send back all messages since <time>
# TODO change this to get with args, k thanks
class api__get_message(Resource):
    def post(self):
        data, response = message_get(request.get_json())
        return data, response


# validates and saves the message sent by user,
#   everything is sent back to the user for debug, in production a successful request will return and empty dict
class api__send_message(Resource):
    def post(self):
        response = message_send(request.get_json())
        return request.get_json(), response



# recieve files from users
#   also sends back debug info for now
class api__send_file(Resource):
    def post(self):
        response = message_send(request.get_json())
        return request.get_json(), response



api.add_resource(index, '/')
api.add_resource(api__send_message, '/api/v0/send/')
api.add_resource(api__send_file, '/api/v0/send_file/')
api.add_resource(api__get_message, '/api/v0/get/')


if __name__ == "__main__":
    app.run(debug=True)
