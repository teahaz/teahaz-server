import sys 
import mesClient as client
import secutity 

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
