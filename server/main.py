import socket
import select

#globals
global PORT
PORT = 8001

global HEADERLEN
HEADERLEN = 20


#basic setup
#server_socket = server_socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("", PORT))
server_socket.listen()

# a list of sockets that are connected to the server
# in the begining its just the server_socket
socket_list = [server_socket]


#recieve a message 
#this NEEDS to be changed
    #it relies on the clinet not sending a too long message
def recieve_message(client):
    try:
        # the header stores the length of the message
        header = client.recv(HEADERLEN)
        
        #if nothing comes then it didnt work
        if not len(header):
            return -1

        #pretty obvious
        mesLength = int(header.decode('utf-8').strip())
        
        #this could be an issue if the message is very long
        print("random print")
        return client.recv(mesLength) 
        
    except:
        # when client disconnects then this gets run
        return -1


def send_message(client, message):
    header = str(len(message))
    header = f"{header:<20}".encode("utf-8")

    client.send(header+message)

    



while True:
    #select.selec(sockets that you can read from[something got sent], sockets to write to[unnecessary], exeption sockets[something with an error])
    read_sockets, somethingApparentlUninportant, exception_sockets = select.select(socket_list, [], socket_list)
    
    #loop through all the sockets that need attention
    for notified_socket in read_sockets:

        # if a new device connected
            #if the socket that need attention is the one open for connections then someone has connected
        if notified_socket == server_socket:

            #accept connection
            client_socket, client_address = server_socket.accept()
            print(f"{client_address} has connected")    

            #on first connection the client sends it name
                #this will be authenticating stuff in later versions
            user = recieve_message(client_socket)
            
            # if user fails to send its name we will just ignore it and continue with the loop
            if user == -1:
                print("authentication of user failed")
                continue

            #add user to users sockets list
            socket_list.append(client_socket)
            print(f"client {client_address} succesfully authenticated")

        #the user has already logged in and is just sending a message
        else:
            
            message = recieve_message(notified_socket)

            #the connection to the client broke
            if message == -1:
                print(f"connection closed from {client_address}")

                #remove from connected sockets list
                socket_list.remove(notified_socket)
                
                #continue the loop
                continue

            #otherwhise send the message on to all other clients
            for client in socket_list:
                if client != notified_socket and client != server_socket:
                    send_message(client, message)

    
    #need to remove the ones from the exeption sockets
    for notified_socket in exception_sockets:
        socket_list.remove(notified_socket)





