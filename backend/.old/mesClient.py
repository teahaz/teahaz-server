import time
import socket


# generally there will be key exchanges here but first version be like
def connect(PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("127.0.0.1", PORT))
        return (s, 100)
    except:
        return -1


#registers the new device on the server
def register(session, username, password):
    socc, key = session
    
    #this is not how a userId will look like in the future
    return time.time()

#logs in on the server, also verifies if the device has been registered and is auth to log in
def login(sessionUnAuth, userId):
    socc, key = sessionUnAuth
    
    #im not exactly sure if this will be name or some id yet but good for now
    name = "rob"

    return (socc, key, name)


def sendMessage(session, message):
    socc, key, name = session
    

    message = f"{name:<50}{message}".encode("utf-8")

    socc.send(message)



def listen(session):
    socc, key, name = session
    while True:
        mess = socc.recv(1024)

        if len(mess) > 5:
            return mess
    

