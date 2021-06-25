from flask import Flask
from flask import request

from flask_restful import Api
from flask_restful import Resource


import os
import base64
import shutil
import hashlib


# inisiate flask
app = Flask(__name__)
restful = Api(app)


def md5sum(filepath: str):
    """ gets md5sum of a file """
    return hashlib.md5(open(filepath,'rb').read()).hexdigest()

def cut(text, num):
    """ Cuts a string to num amount of chars """
    return text[:num]

def encode(a):
    " base64 encode "
    return base64.b64encode(str(a).encode('utf-8')).decode('utf-8')

def decode(a):
    " base64 decode "
    return base64.b64decode(str(a).encode('utf-8')).decode('utf-8')


def check_create(path):
    """ checks if a folder exists, and if not then creates it """
    if not os.path.exists(path):
        os.mkdir(path)


def checkpw(username, password):
    """ Checks if the user has access to a file """

    # password is stored in a file (hashed and encoded)
    with open(f"storage/userdata/{username}/accesspw", 'r')as infile:
        stored = infile.read()

    # stored doesnt have to be decoded bc password is encoded before this
    if stored == password:
        return True
    return False




class data(Resource):
    def post(self, username):
        """ Upload file """

        # get data
        ## Cut lengths to 100, 100 and 1 000 000 (one megabyte) respectively
        username = encode(cut(username, 100))
        password = encode(cut(request.get_json().get('password'), 100))
        data = encode(cut(request.get_json().get('data'), 1000000)) # one megabyte


        # Auth user so they cannot overrwite someone elses data without the password
        if os.path.exists(f'storage/userdata/{username}'):
            if not checkpw(username, password):
                return "Permission Denied: You do not have access to this file, try sending a password or using a different username", 401
        else:
            os.mkdir(f'storage/userdata/{username}')


        # write password
        with open(f'storage/userdata/{username}/accesspw', 'w+')as outfile:
            outfile.write(password)

        # write data
        with open(f'storage/userdata/{username}/data', 'w+')as outfile:
            outfile.write(data)

        # write checksum
        ## the checksum is stored so it doesnt have to be calculated every time a user requests it
        checksum = md5sum(f"storage/userdata/{username}/data")
        with open(f'storage/userdata/{username}/hash', 'w+')as outfile:
            outfile.write(checksum)

        return {
                "type": "md5",
                "hash": checksum
                }, 200



    def get(self, username):
        """ Download stored file """

        # check data
        if not username:
            return "Username was not part of the url", 400
        if request.headers.get('password') == None:
            return "No value supplied for required field 'password'"


        # get data, and cut to max lengths
        username = encode(cut(username, 100))
        password = encode(cut(request.headers.get('password'), 100))

        # check if file exists
        if not os.path.exists(f'storage/userdata/{username}'):
            return "Path does not exist", 404

        # check password
        if not checkpw(username, password):
            return "Permission Denied: You do not have access to this file, try sending a password or using a different username", 401

        # read data
        with open(f'storage/userdata/{username}/data', 'r')as infile:
            data = infile.read()

        return data, 200



    def delete(self, username):
        """ Delete all data on username """

        # get data
        username = encode(cut(username, 100))
        password = encode(cut(request.headers.get('password'), 100))


        # check if file exists
        if not os.path.exists(f'storage/userdata/{username}'):
            return "Path does not exist", 404


        # check password
        if not checkpw(username, password):
            return "Permission Denied: You do not have access to this file, try sending a password or using a different username", 401


        # delete users directory
        try:
            shutil.rmtree(f"storage/userdata/{username}")
            return "OK", 200

        # delete failed?
        except Exception as e:
            return f"Failed to delete user data: {e}", 500



class checksum(Resource):
    def get(self, username):
        """ Get checksum of file on server """

        # check data
        if not username:
            return "Username was not part of the url", 400
        if request.headers.get == None:
            return "No value supplied for required field 'password'"


        # format, encode data
        username = encode(cut(username, 100))
        password = encode(cut(request.headers.get('password'), 100))


        # check if file exists
        if not os.path.exists(f'storage/userdata/{username}'):
            return "Path does not exist", 404


        # check password
        if not checkpw(username, password):
            return "Permission Denied: You do not have access to this file, try sending a password or using a different username", 401


        # read hash
        with open(f'storage/userdata/{username}/hash', 'r')as infile:
            checksum = infile.read()


        return {
                "type": "md5",
                "hash": checksum
                }, 200


# endpoints
restful.add_resource(data, '/storage/<username>', '/storage/<username>/')
restful.add_resource(checksum, '/storage/<username>/hash', '/storage/<username>/hash/')


# make sure storage folders exist
check_create('storage')
check_create('storage/userdata')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=13338, debug=True)
