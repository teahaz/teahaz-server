# request structure
requests will send json data with them

the following are examples of how to structure messages
### POST message
```json
// endpoint: /messages
{
    "username": "<username>",
    "cookie": "<cookie>",
    "type": "text",
    "message": "<text based message>",
    "chatroom": "<chatroom_id>"
}
```

### POST file
```json
// endpoint: /files
{
    "username": "<username>",
    "cookie": "<cookie>",
    "type": "file",
    "mimetype": "<mimetype [not file extension]>",
    "chatroom": "<chatroom_id>"
}
// file should be attached with the http post files method
```


### GET messages
```json
// endpoint: /messages
{
    "username": "<username>",
    "cookie": "<cookie>",
    "time": "<time since last get>"
    "chatroom": "<chatroom_id>"
}
```


### GET files
```json
// endpoint: /files
{
    "username": "<username>",
    "cookie": "<cookie>",
    "filename": "<uuid>",
    "chatroom": "<chatroom_id>"
}
```



# server responses
server will also respond with json

some example responses
### response for GET messages
```json
[
    {   // type == text
        "sender_username": "<sender_username>",
        "send_time": "<time>",
        "type": "text",
        "message": "<message>",

    },
    {   // type == file
        "sender_username": "<sender_username>",
        "send_time": "<time>",
        "type": "file",
        "filename": "<uuid>",
        "mimetype": "<mimetype>",

    },
    {   // type == text
        "sender_username": "<sender_username>",
        "send_time": "<time>",
        "type": "text",
        "message": "<message>",

    },
]
```
### response for GET files
the file lmao



# database
switching everything over from storing in files to storing as a database, this should help solve multiple issues
ideas on how the database will work
    - running a database server inside the docker container {benefits: `works neater/fast`, problems: `hard to setup, non persistant after the docker exits`}
    - mongo dbk
    - use sqlite

DEPRICATED -- no longer true just kept here for reference
i will not use mongo db in favour of sqlite: for now i think i will do mongo db, where there will be groups like this
    - users group: {username: `username`, password: `hashed bcrypt will handle salt i thin`, cookie: `will probably change often but best if stored here` }
    - group for each conversation with documents like this: {time: `time`, sender: `sender username`, message: `message/null in case of file send`, file: `path to saved file/null if its a text` }
!DEPRICATED



### sqlite
for now i will use sqlite, bc i can make persistant storage in local files
inside the folder */server/storage* there is a pre defined folder structure
``
/server/storage/
|
|-users.db
|
|-conv1 // a folder for each chatroom on the server
|    |
|    |-- messages.db
|    |
|    |
|    |-- members.db
|    |
|    |
|    |--uploads
|          |
|          |
|          |- filehash.extention_random-value //using this weird format to avoid any weird name issues, like path traversal or colliding names
|          |
|          |- filehash.extention_random-value //using this weird format to avoid any weird name issues, like path traversal or colliding names
|
|-conv2 // a folder for each chatroom on the server
|    |
|    |-- messages.db
|    |
|    |
|    |-- members.db
|    |
|    |
|    |--uploads
|          |
|          |
|          |- filehash.extention_random-value //using this weird format to avoid any weird name issues, like path traversal or colliding names
|          |
|          |- filehash.extention_random-value //using this weird format to avoid any weird name issues, like path traversal or colliding names
``
- chatroom names might be a uuid or a hash of some sorts, this will be figured out with time
- file-hashes might also be changed to a uuid so because of pythons slow math engine

+ making connections
for now i will make a connection to the sqlite server [local file] each time it is needed
yes this will probably add latency, and yes i will change this but for simplicity it will be like this for now


### sqlite version2
for now i will use sqlite, bc i can make persistant storage in local files
inside the folder */server/storage* there is a pre defined folder structure
``
/server/storage/
|
|
|
|
|
|
|-chatrooms.db
    |
    |-conv1 e
    |    |
    |    |-- messages.db
    |    |
    |    |
    |    |-- members.db
    |    |
    |    |
    |    |--uploads
    |          |
    |          |
    |          |- filehash.extention_random-value //using this weird format to avoid any weird name issues, like path traversal or colliding names
    |          |
    |          |- filehash.extention_random-value //using this weird format to avoid any weird name issues, like path traversal or colliding names
    |
    |-conv2 // a folder for each chatroom on the server
    |    |
    |    |-- messages.db
    |    |
    |    |
    |    |-- members.db
    |    |
    |    |
    |    |--uploads
    |          |
    |          |
    |          |- filehash.extention_random-value //using this weird format to avoid any weird name issues, like path traversal or colliding names
    |          |
    |          |- filehash.extention_random-value //using this weird format to avoid any weird name issues, like path traversal or colliding names
``
- chatroom names might be a uuid or a hash of some sorts, this will be figured out with time
- file-hashes might also be changed to a uuid so because of pythons slow math engine

+ making connections
for now i will make a connection to the sqlite server [local file] each time it is needed
yes this will probably add latency, and yes i will change this but for simplicity it will be like this for now



# users and login
2 main ideas
1. users could be logged in to a server where there are multiple chatrooms are available, the users can be authorised to use different ones
    in this case users.db would be where it is, and there would be a members.db inside the chatroom folder to indicate who has access to the chatroom
2. each chatroom could have their own set of users and maybe a chatroom password.
    in this case users.db would not exist, and members.db would include passwords and cookies
3. probably winning idea
    - there is one central `users.db` which stores user data like {`usernames`, `passwords`, `chatrooms`:[`list`, `of`, `active`, `chatrooms`]}
    - there will be a folder for each chatroom which has multiple files
        - `messages.db` stores messages, with {'username', 'type=text/file/both', 'message(base46/encryption)', 'path/to/file'}
        - `members.db` should store a refrence of active members so its stored in more than one place
        - `uploads/` a folder containing all files with uuid/hash names and encrypted/base64 (file extentions should either be in the file or should show for convenience)


# TODO
- error check the json in api.py
    - error on all but no cookie, which should go to /auth
- find a better var name for `response` in api.py [saving stuff in the database]
- find better name for helpers
