import sys
import time
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




############################## important ##########################
#the stuff before was just copied from above

###
#syntax:
#    this clinet.get() takes 2 arguments,
#    arg1 = session
#    arg2 = the time when the last message was recieved:
#        this means that all messages that shouldve come through since that time will be downloaded
#
#        IMPORTANT: time should be in epoch format(unix time) 
#        time.time does this automatically: [import time; time.time()]
#
#        tim should also be in float format ( this is the default)
#





print("attempting to get messages")
#get messages since epochtime [1589379287.4890685]
lastGetTime = 1589789732.4058611
missedMessages = client.get(session, lastGetTime) 
print(missedMessages)




