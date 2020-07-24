# i made a commented example of how to use the new auth method
import sys 
import mesClient as client
import security 
import json 

# some vars that are needed later on
ip = "127.0.0.1"
port = 8001

# this is where security.auth will save creds
# the username wont be encrypted so you can use it for autologin
saved_user_credentials = "./.creds"

# just so it dont error out in my shitty way of calling auth
# dont worry about it
username = ""
password = ""


auth_type = input("first login? [t/f]")
# method for first login where you need to specify username and password
# this should probably be automatic so you dont have to ask the user, but you also probably know this bc you are better att making a good user experince
if auth_type == "t":
    # i didnt add this inside of auth bc i think you would want to style it better
    # it is in this if statememnt bc you dont necessary need as after a login the creds will be saved by security.auth
    username = input("username: ")
    password = input("password: ")

    # this is needed for security.auth
    auth_type = True


# method for autologin
elif auth_type == "f":
    # although this file is mainly handled by security.auth() we need the username from here to avoid saving it twice
    with open(saved_user_credentials, "r")as infile:
        creds = infile.read()

    # username is stored in json 
    creds = json.loads(creds)
    username = creds["username"]

    # this is needed for security.auth
    auth_type = False

else:
    print("invalid option")
    sys.exit()


# this has been standard from before
session = client.connect(username, ip, port)

# check if session returned nothing
if not session:
    print("error connecting to client")
    sys.exit()

# this tests if the socket was made properly, yes i did turn a bug into a useful feature, 
    # id doesnt matter what text is in here as long as its not too long
client.send(session, "this is for testing if the socket works, i think this will later be client.test_socket")



# very important, im going to paste the explinatin for these args here that i wrote a while back so that might explain a sift in tone
    # also i way to lazy to read it over

# explination of all this shit
# 1, session is manditory
# 2, the first time the user connects [s]he will give a username and a password, a hashed password and a plain text username will be stored in the `path_to_saved_creds` 
    # so password_auth== True when the user has not been authenticated on this device yet(does not have a creds file), otherwhise it should be false
    # the reason for username not being hashed is that this way the saved_creds file can store the username displayed to others as well as be used for automatic logins
# 3, 4 should be obvi, they are only taken into account if password_auth is True
#5 is the path to the creds file, ofc this could be anywhere i just set './.creds' as a default. you can change it however you like, knock yourself out
    #IMPORTANT path_to_saved_creds is needed when using password_auth as well, in this case the passowrd in path_to_saved_creds will be overwritten by a new one
security.authenticate(session, password_auth=auth_type, username=username, password=password, path_to_saved_creds="./.creds")




## some basic tests start here

# we should get all messages since the time of last login
print("attempting to get messages")
lastGetTime =1589969514.155710
missedMessages = client.get(session, lastGetTime) 
print(missedMessages)



# and thsi part you should be familiar with, selecting if you want to listen or send
    # you will probably re write this anyway
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


