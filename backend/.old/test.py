#this program is just as an example of how to user the mesClient module
import threading
import mesClient as client

#the port specifies the texting channel  that you are in
PORT = 8000


######################################################## connect ############################################
#initial connection to server
#sessioniUnAuth is a session id that is not logged in
sessionUnAuth = client.connect(PORT)
if sessionUnAuth == -1:
    print ("failed to connect to server")
else:
    print("connection succ")

    #debug
    print(sessionUnAuth)




######################################################## register ############################################
#if a device logs in for the first time it will need to get a 'cookie'
cookie =  client.register(sessionUnAuth, "username", "password")
#cookie should be saved in some secret file
#it is used when logging in
#register does NOT log in
if cookie == -1:
    print("registration of device failed")
    print("are you sure the username and password are correct?")
    print("and some other bs they usually put here")
else:
    print("registration succ")

    #debug
    print(f"cookie = {cookie}")




######################################################## login ############################################
#for registered devices cookie should be in some file already
session = client.login(sessionUnAuth, cookie)
#the session will be the users cookie, it has his name the socket pointer and his encryption key in it
if session == -1:
    print("login failed")
else:
    print(f"login succ")

    #debug
    print(f"session = {session}")

#once the user has logged in he can start communicating with the server


################################################## listen #################################################
# this function listens for a message and returns it
# the intetnion is to run this on a seperate thread in a while loop, instantly printing the message
# this way new can be instantly delivered
# if its not listening when a message arrives then the message will get lost and the server will try to resend it until it arrived
def listen(session):
    while True:
        message = client.listen(session)
        #incomming messages definatly need to be formatted a bit
        print(message.decode("utf-8"))

listen(session)

x = threading.Thread(target=listen, args=(session,))
x.start


###################################################### send message ########################################
# i mean i hope this one is obvious
ret = client.sendMessage(session, "message")
#message will return 0 on no error -1 on error
if ret == -1:
    print("send failed")
else:
    print("message sent")

while True:
    message = input()
    ret = client.sendMessage(session, message)
    #message will return 0 on no error -1 on error
    if ret == -1:
        print("send failed")
    else:
        print("message sent")


