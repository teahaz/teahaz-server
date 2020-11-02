import time
import base64
import json
import sqlite3

import helpers
from helpers import decode_messages as d



# method will validate user, decrypt [if this dont end up being e2ee] and store
# method wont make any difference between a file and a textmessage [maybe for big files idk, its my server i can store all this in one file if i want]
def message_send(json_data):
    username = json_data['username']
    cookie = json_data['cookie']
    message = json_data['message']
    message_type = json_data['type']
    timenow = str(time.time())

    #obvi not yet implemented
    if not helpers.authenticate(username , cookie):
        return 401, "unauthorized"

    # storing the usual one line json_data that i have been doing before 
    token = {'time':timenow, 'username': username, 'type':message_type, 'message': message}
    with open('db/notadatabase', 'a+')as outfile:
        outfile.write(json.dumps(token)+'\n')

    return 200, "ok"




def message_get(json_data):
    username = json_data['username']
    cookie = json_data['cookie']
    last_time = json_data['last_get_time']
    convId = json_data['convId']

    # checks if user is authenticated
    if not helpers.authenticate(username, cookie): return 401, "unauthorized"
    #check if conversation exists, and if user has permission
    if not helpers.is_valid_chatroom(convId, username, cookie): return 403, "chatroom doesnt exist or not authorized"


    print(d(username), d(cookie), d(last_time), d(convId))
    return 200, json_data




def upload_file(json_data):
    return 200, 'filename'


def download_file(json_data):
    return 200, 'filename'
