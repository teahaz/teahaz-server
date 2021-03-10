This is a long read, you may need some tea!  :)

# overview
Teahaz offers both an official server and the means to host your own.


### basic server structure
Each server is responsible for handling multiple chatrooms.
![image of server structure](images/single_server_base_nice.png)

The server manages each chatroom individually. It doesnt store any centralized data but lets each chatroom manage their own database with their own users, channels, settings, etc. In effect each chatroom is its own segregated server-like system.


