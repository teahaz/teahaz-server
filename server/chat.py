import socket
import select

header = 0xf
ip = ""
port = 8001

#basic setup
#socc = server_socket
socc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socc.bind((ip, port))
socc.listen()


#a list of all sockets that are connecting including socc
sockets_list = [socc]

clients = {}

def recieve_message(client_socket):
    try:
        message_header = client_socket.recv(header)

        if not len(message_header):
            return False

        message_len = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_len)}

    except:
        print("malformed packet recieved from client")

while True:
    #selsect.select(socketsToReadFrom, socket_to_write_to, socekts_that_error)
    read_sockets, somethingApparentlUninportant, exception_sockets = select.select(sockets_list, [], sockets_list)
    for notified_socket in read_sockets:
        #not exactly sure how but this means that someone just connected and we need to handle that
        if notified_socket == socc:
            client_socket, client_address = socc.accept()
            print("connection accepted")

            #need to get username from client
            user = recieve_message(client_socket)
            #if user disconnected
            if user is False:
                continue

            #add user to sockets list
            sockets_list.append(client_socket)
            #add user to sockets dictionary
            clients[client_socket] = user
            
            print(f"accepted new connection from {client_address[0]}:{client_address[1]} ==> {user['data'].decode('utf-8')}")
        
        #if the user was already connected
        else:
            message = recieve_message(notified_socket)

            #socket connection closed
            if message is False:
                print(f"closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            
            #recieve_message
            user = clients[notified_socket]
            print(f">{user['data'].decode('utf-8')} ===> {message['data'].decode('utf-8')}")
           
            #distribute the message to all the users
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        socket_list.remove(notified_socket)
        del clients[notified_socket]
