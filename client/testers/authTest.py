import sys 
import mesClient as client
import security 

ip = "127.0.0.1"
port = 8001


username = input("username: ")
password = input("password: ")


session = client.connect(username, ip, port)

if not session:
    print("error connecting to client")
    sys.exit()

client.send(session, "this is for testing if the socket works, i think this will later be client.test_socket")


security.authenticate(session, password_auth=True, username=username, password=password, path_to_saved_creds="./.creds")


print("attempting to get messages")
lastGetTime =1589969514.155710
missedMessages = client.get(session, lastGetTime) 
print(missedMessages)



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


