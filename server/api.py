import time
import base64
import json
from file_read_backwards import FileReadBackwards


def validate(username, cookie):
    return True


# method will validate user, decrypt [if this dont end up being e2ee] and store
# method wont make any difference between a file and a textmessage [maybe for big files idk, its my server i can store all this in one file if i want]
def message_send(json_data):
    # im not sure i need all this but its just here for now
    username = json_data['username']
    cookie = json_data['cookie']
    message = json_data['message']
    message_type = json_data['type']
    timenow = str(time.time())

    #obvi not yet implemented
    if not validate(username , cookie):
        return 403

    
    # storing the usual one line json_data that i have been doing before 
    token = {'time':timenow, 'username': username, 'type':message_type, 'message': message}
    with open('db/notadatabase', 'a')as outfile:
        outfile.write(json.dumps(token)+'\n')

    return 200

    

def message_get(json_data):
    # im not sure i need all this but its just here for now
    #username = json_data['username']
    #cookie = json_data['cookie']
    last_get_time = int(float(base64.b64decode(json_data['last_get_time'])))

    # each needed line will be appended to this and then returned
    data = ""


    with FileReadBackwards('db/notadatabase' , encoding="utf-8") as frb:
        while True:
            #read until file has ended
            l = frb.readline()
            if not l:
                break

            
            #after each \n check the time
            line = json.loads(l)
            senderTime = int(float(line["time"]))

            if senderTime < last_get_time:
                break

            data += l 

        return base64.b64encode(data.encode('utf-8')).decode('utf-8'), 200



