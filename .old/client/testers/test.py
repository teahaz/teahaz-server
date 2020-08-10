########################################################################
# a small test app to demonstrate how to use the client module
########################################################################

import sys
import mesClient as client


#some basic setup
#obvi the ip would be butorhaz in the future
ip = "127.0.0.1"
port = 8001


# login details will change in the future
###  for now i just set a name
### the intetion is that if its your first time one the device you need to give some login and password
### to avoid doing this too  much after the first login there should be some id saved
### for now its just this tho
loginDetails = input("hand over your name: ")


# connecting to the sever
### you recieve a session cookie, this is needed for all communications with the server
session = client.connect(loginDetails, ip, port)
# error checking is important
if session == 0:
    print("[ERROR] connection to server faliled [636c69-636f6e6e-01]")
    sys.exit(-1)

#i will solve this later but fore now this is necessary for some timing issue so just accept it for now
client.send(session, loginDetails)


#this line is ony so that i didnt need to make a seperate test app for the listening and sending aspect
l = input("is this instant listening or sending: [s/l]")

#listen 
#this loop listens for a message and instantly prints in
# it is intended to run on a seperate thread
if l == "l":
    while True:
        # client.listen listens until it gets a messge and it returns either that or an error
        a = client.listen(session)
        
        # these arent necessary true, you can never tell why a socket fails but usually they are good
        if a == -1:
            print("[ERROR] connection closed [636c69-6c697374-03]")
            sys.exit(-1)
        elif a == -2:
            print("[ERROR] malformed packet recv from server [636c69-6c697374-04]")
            sys.exit(-1)
        else:
            print(a.decode("utf-8"))




# send is pretty self explanetory
# current limitations:
    # messages need to be loaded into memory of both the client and the server
    # this means that dont send larger messages then the server could handle
elif l == "s":
    while True:
        mes = input(">>  ")

        #send will only return error messages
        a = client.send(session, mes)

        #in general do 2 sends before erroring out just incase
        #error handling
        if a == -1:
            print("[ERROR] format error, malformed message  [636c69-73656e64-05]")
            sys.exit(-1)
        elif a == -2:
            print("[ERROR] failed to send message to server  [636c69-73656e64-06]")
            sys.exit(-1)


