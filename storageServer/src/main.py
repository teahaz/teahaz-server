from flask import Flask

from flask_restful import Api
from flask_restful import Resource


import os
import base64


# inisiate flask
app = Flask(__name__)
restful = Api(app)


def encode(a):
    " base64 encode "
    return base64.b64encode(str(a).encode('utf-8')).decode('utf-8')

def decode(a):
    " base64 decode "
    return base64.b64decode(str(a).encode('utf-8')).decode('utf-8')





class data(Resource):
    def post(self, username):
        """ Upload file """

        # security ++
        username = encode(username)





    def get(self, username):
        """ Download stored file """
        pass


class checksum(Resource):
    def get(self, username):
        """ Get checksum of file on server """
        pass


restful.add_resource(data, '/storage/<username>/data/', '/storage/<username>/data')
restful.add_resource(checksum, '/storage/<username>/hash/', '/storage/<username>/hash')



def setup():
    if not os.path.exists('storage'):
        os.mkdir('storage')

    if not os.path.exists('storage/userdata'):
        os.mkdir('storage/userdata')


setup()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=13338, debug=True)
