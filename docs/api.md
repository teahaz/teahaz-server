API documentation v0
====================
***NOTE:*** This is not proper documentation, but a very basic description of the api.
**NOTE2:** Typed this on the bus so idk how good quality this all is. :)



Available methods:
-----------------

* chatroom
url: `/api/v0/chatroom`

* login
url: `/api/v0/login/<chatroomID>`

* users
url: `/api/v0/users/<chatroomID>`

* channles
url: `/api/v0/channels/<chatroomID>`

* messages
url: `/api/v0/messages/<chatroomID>`


<br />
<br />

More detail on some variables.
-----------------------------

### userID
type: uuid (str) || '0'
This is a unique identifier of each user, assigned by the server. In a normal case this is a uuid similar to all other identifiers, however in the case of the classroom constructor this ID will always be `"0" (str)`


### username:
type: str
This used to be the `nickname` of the user, it can be freely changed, and has no meaning on the server-side. However this is the name that should be displayed to other users.
When talking to the server, a user should be refered to by their `userID`

### password:
type: str
The users password.


### chatroomID:
type: UUID (str)
A unique ID assigned to each chatroom at creation. These are assigned by the server, and returned when the chatroom is created.
The server does not understand chatroom names and chatrooms should be refered to by their `chatroomID`.


### chatroom\_name:
type: str
The name of a chatroom. Similar to `username` this is a sort of "nickname" and when talking to the server, the chtroom should be refered to by its `chatroomID`.


### channels:
type: Array of objects (list of dicts) 

A list of channels and all their details.
Channels on teahaz are similar to channels on discord as in they are sperate streams of messages, athat can have independant permissions for different groups of people.


Example of a channel object:

```js
{
    {
        channel_name": "default",
        channelID": "UUID (str)",
        public: Bool,
        permissions: {
            r: Bool,
            w: Bool,
            x: Bool
            }
    }
}
```

#### channel\_name:
type: str
This is the name of the channel. Similarly to all other names this doesnt have a meaning on the server, and the channel should be refered to by its `channelID`.

#### channelID
type: UUID (str)
Unique identifier of a channel.


#### permissions
type: object (dict)

This object represents the permissions your user has over a channel. This uses a slightly unix like syntax of useing `r w x` for read write and admin (execute).

* r (read)
type: Bool
Permission to read messages.
This permission also sets whether the user has the ability to see the chatroom, and to interact with it in any way.

* w (write)
type: Bool
Permission to write messages.


* x (admin)
type: Bool
Executive or admin permission.
This permission allows you to manage other users messages in the channel, as well as some other admin features.
    (none of this has been implemented yet)



#### public
type: Bool
Shorthand for rw and x being true.
**NOTE:** This is only temporary fix for some backend stuff, and will be removed when classes work. Dont really rely on / use it



### colour:
type: obj (dict)
The colour object represents a user settable colour.
The colour is broken down into rgb values, each value can have an integer from 0-255 or `null` for unset.

```js
        colour: {
            r: int || null,
            g: int || null,
            b: int || null
            }
```

These colours cannot be changed **yet**.

### messageID:
type: UUID (str)
Unique Identifier of each message


### replyID:
type: UUID (str)
This is an optional field in the message obj. If set the message is considered as a reply. The replyID has to be set to the `messageID` of another message.


### data:
type: str
This is the body of a message. It can hold multiple values, including:

* encoded (later encrypted) string in the case of a message sent from one user to another.
* un-encoded string in the case of a system message from the server
* UUID in the case of a file, this UUID would be a fileID for a file that got sent to the server.



<br />

other information
-----------------


### headers vs json\_data
On all `GET` requests json has to be embedded in the request header because the http spec does not allow sending data in those requests. In all other reqests, variables has to be sent in the http data field (or `json=` with python requests)

<br />

### \<chatoomID\> at the end of url
When you see \<chatroomID\> at the end of a url, its because the ID of a chatroom has to be part of the path. (without the \< \> symbols)

eg: ` /api/v0/login/847e5380-d656-11eb-8c72-69e0783d7026 `

<br />

### Login / register operations taking long
This is an unfortunate feature of using strong hashing for passwords. Whenever passwords are sent, it takes a couple seconds to save/verify them because of the hashing used. (`bcrypt`)


<br />

### Cookies.
All methods that dont set a cookie for the user (ie: different forms of login and register) require a cookie header to be set.

Cookie format: 
```
<chatroomID>=<cookie>
// <cookie> is a UUID assigned by the server
```
Most http libraries (like python reqests) should handle cookies automatically.


### status codes
A list of status codes used by the server:

200: OK
400: user error
401: not logged in
403: Permission denied (usually trying to access something your user does not have permission to)
500: Server error (you did nothing wrong, please report it to me! )

Hopefully I didnt miss anything.

<br />
<br />
<br />


# More detail on methods

## chatroom
url: `/api/v0/chatroom`

### post
action: Create a new chatroom.

needed data: 
```js
{
    username: "string",
    password: "string",
    chatroom_name: "string"
}
```

example data returned:
```js
{
    chatroom_name: "string",
    chatroomID: "UUID (str)",
    channels: [
            {
                channel_name: "default",
                channelID": "UUID (str)",
                public: Bool,
                permissions: {
                    r: Bool,
                    w: Bool,
                    x: Bool
                    }
            }
        ],
    "userID": userID
    }
}
```

**This method sets a cookie**.

<br />


## login
url: `/api/v0/login/<chatroomID>`

### post
action: Login to a chatroom.

***NOTE***: This requires you to already have an account.

needed data:
```js
{
    userID: "UUID (str)",
    password: "string"
}
```

example data returned:
```js
{
    chatroomID: "UUID (str)",
    userID:  "UUID (str)",
    channels: [
        {
            channel_name": "default",
            channelID": "UUID (str)",
            public: Bool,
            permissions: {
                r: Bool,
                w: Bool,
                x: Bool
                }
        },
        {
            channel_name": "string",
            channelID": "UUID (str)",
            public: Bool,
            permissions: {
                r: Bool,
                w: Bool,
                x: Bool
                }
        }
    ]
}
```
**This method sets a cookie**.

### get
action: Check if you are logged in.

needed data:
```js
    userID: "UUID (str)"
```

There is no useful data returned by this, other than a status code to indicate whether or not you are logged in.

status code 200 == logged in
status code 401 == not logged in







## users
url: `/api/v0/users/<chatroomID>`

### get
action: Get all users of a chatroom

This method returns all the users of the chatroom. In the future I will add an option to filter this to users with read access to a specific channel. (kinda discord like)


needed data:
```js
    userID: "UUID (str)"
```


example return:
```
[
    {
        userID: '0' || 'UUID (str)',
        username: "string",
        colour: {
            r: 0,
            g: 0,
            b: 0
            }
    }
]
```

## channles
url: `/api/v0/channels/<chatroomID>`

### post
action: Create a new channel

needed data:
```js
    userID: "UUID (str) || '0'",
    channel_name: "string",
```


example return:
```js
{
    channelID: "UUID (str)",
    channel_name: "string",
    public: True,
    permissions:
        {
            r: Bool,
            w: Bool,
            x: Bool
        }
}
```

### get
action: Get all channels the user has read access to

needed data:
```js
    userID: "UUID (str) || '0'"
```

example return:
```js
[
    {
        channelID: "UUID (str)",
        channel_name: "string",
        public: True,
        permissions:
            {
                r: Bool,
                w: Bool,
                x: Bool
            }
    },
    {
        channelID: "UUID (str)",
        channel_name: "string",
        public: True,
        permissions:
            {
                r: Bool,
                w: Bool,
                x: Bool
            }
    },
]

```

## messages
url: `/api/v0/messages/<chatroomID>`

### post
action: send message to chatroom/channel

needed data:
```js
    userID: "UUID (str) || '0'",
    channelID: "UUID (str)",

    replyID: "UUID (str)" (optional)

    data: "String (your message)"
```


example response:
```js
{
    messageID: "UUID (str)"
}
```

### get
action: Get message

needed data:
```
    userID: "UUID (str) || '0'",

    count: int <100           (optional),
    time: float (time.time()) (optional),
    channelID: "UUID (str)"   (optional)
```

By default this method returns the 10 latest messages, looking in all channels that are available to the user.

optional arguments:
* count:
type: int
The number of messages to be returned. The current maximum is 100

* time:
type: float
If this is set then the server only looks for messages that got sent before the `time` varibale. (epoch time format)


* channelID
type: "UUID (str)"
If this is set then the server will only look in the specified channel for messages.



<br />
<br />
<br />
<br />
<br />
<br />
<br />
<br />
<br />
<br />
<br />
<br />
<br />
<br />



































<!--
docs of /api/v0
==============

## Table of Contents
1. [/message/](#messages)
2. [/file/](#files)
3. [/chatroom/](#chatrooms)
    - [Creating a new chatroom](#Creating-a-new-chatroom)
5. [/invites/](#invites)
    - [Creating an invite](#Creating-an-invite)
    - [Using an invite](#Using-an-invite)





messages
========
The messages object representes the man stream of data that the client needs to be aware of. This includes messages, files, system messages, etc.
The server currently stores 9 values for each message:

* time
    - the time when the message was sent
* messageId
    - a unique Id for each message assigned by the server
* replyId
    - An Id that can be set by the user to any other message's Id
    - The value should be `null` if the message is not a reply to another message
* username
    - The username of the person who sent the message
* nickname
    - The nickname/display name of the user who sent the message
* type
    - The type of the message
    - supported types:
        - text
        - file: file sent by user
        - system: automatic messages from the server, depending on userconfig these should be displayed because they could have security impacts
        - system-silent: same as above but not so relevant, probably should not be displayed (tho should be accesible to the user, either by toggle or a sperate screen)
        - delete: A message has been deleted, It should be removed from the local cache aswell
* message
    - The text/body of the message
    - This will be encrypted
* fileId
    - The id of a file sent
    - This id is used as a filename on the server side, and is needed to download any file
* filename
    - The original filename of a file


### Types of messages

####  text:
A standard text/message from a user.

example:
```json
// following is an example of a message, and a reply to the first message
[
    { 
        "time": 1618262186.309995,
        "messageId": "5730800e-9bd4-11eb-acec-b42e99435986",
        "replyId": null,
        "username": "cool person",
        "nickname": "cool displayname",
        "type": "text",
        "message": "QWNjb3JkaW5nIHRvIGFsbCBrbm93biBsYXdzCm9mIGF2aWF0aW9u",
        "fileId": null,
        "filename": null,
        "filesize": null
    },
    {
        "time": 1618262875.8404057,
        "messageId": "f22e7b00-9bd5-11eb-a872-b42e99435986",
        "replyId": "5730800e-9bd4-11eb-acec-b42e99435986",
        "username": "a",
        "nickname": "a",
        "type": "text",
        "message": "dGhlcmUgaXMgbm8gd2F5IGEgYmVlCnNob3VsZCBiZSBhYmxlIHRvIGZseS4=",
        "fileId": null,
        "filename": null,
        "filesize": null
    }
]
```

<br />
<br />

#### delete:
When a message is deleted it gets removed from the database but could still be in a users cache. This message is an indicaton to the clent that it should remove the message.
(this message probably shouldnt be displayed to the end user)


example:
```json
[
    {
        "time": 1618263099.53122,
        "messageId": "778300f0-9bd6-11eb-93de-b42e99435986",
        "replyId": null,
        "username": "a",
        "nickname": "a",
        "type": "delete",
        "message": "f22e7b00-9bd5-11eb-a872-b42e99435986",
        "fileId": null,
        "filename": null,
        "filesize": null
    }
]
```

other types have not yet been implemented



<br />
<br />

Getting all messages since \<time\>
---------------------------------
This method should return all messages in a chatroom that were sent since the time variable. This method serves as the primary way to get messages back form the api, as it allows users to get many messages at once.


### Endpoints:
* GET: `http(s)://url:port/api/v0/messasge/<chatroomId>`
`<chatroomId>` should be replaced by the ID of the chatroom
<br />


### Required fields:
* username
* chatroomId
* time
    - The time variable should be in epoch/unix time.

<br />

### Code example:

```py

url = http:/<server url>/api/v0/message/" + chatroomId

headers = {
    "username": "best_user",
    "time": "946681200.23243"
}


#NOTE get methods need to have data in the header field and not json
res = session.get(url=url, headers=headers)

print("status_code: ", res.status_code)
print(res.text)
```

<br />


### Example output:

```json
[
    {
        "time": 1617028913.9485404,
        "messageId": "e7944966-909c-11eb-a14c-b42e99435986",
        "replyId": null,
        "username": "a",
        "nickname": "a",
        "type": "text",
        "message": "QWNjb3JkaW5nIHRvIGFsbCBrbm93biBsYXdzIG9mIGF2aWF0aW9uLCB0aGVyZSBpcyBubyB3YXkgYSBiZWUgc2hvdWxkIGJlIGFibGUgdG8gZmx5Lg==",
        "fileId": null,
        "filename": null
    },
    {
        "time": 1617028927.8282716,
        "messageId": "efda2a96-909c-11eb-bd2f-b42e99435986",
        "replyId": null,
        "username": "a",
        "nickname": "a",
        "type": "text",
        "message": "SXRzIHdpbmdzIGFyZSB0b28gc21hbGwgdG8gZ2V0IGl0cyBmYXQgbGl0dGxlIGJvZHkgb2ZmIHRoZSBncm91bmQu",
        "fileId": null,
        "filename": null
    },
    {
        "time": 1617028941.5795443,
        "messageId": "f80c717e-909c-11eb-b2a3-b42e99435986",
        "replyId": null,
        "username": "a",
        "nickname": "a",
        "type": "text",
        "message": "VGhlIGJlZSwgb2YgY291cnNlLCBmbGllcyBhbnl3YXkgYmVjYXVzZSBiZWVzIGRvbid0IGNhcmUgd2hhdCBodW1hbnMgdGhpbmsgaXMgaW1wb3NzaWJsZS4g",
        "fileId": null,
        "filename": null
    }
]
```



<br />
<br />


Getting messages by messageId
-----------------------------
This method should return one message, with the messageId that the client supplied. The purpose of this method is to look up individual messages for example as a way to get a reply.



### Endpoints:
* GET: `http(s)://url:port/api/v0/message/<chatroomId>`
`<chatroomId>` should be replaced by the ID of the chatroom
<br />

### Required fields:
* username
* messageId
* chatroomId

<br />

### Code example:

```py

url = http:/<server url>/api/v0/message/" + chatroomId

headers = {
    "username": "best_user",
    "messageId": "8b7f3eba-81b0-11eb-97e5-655df6aeb2ec"
}


#NOTE get methods need to have data in the header field and not json
res = session.get(url=url, headers=headers)

print("status_code: ", res.status_code)
print(res.text)
```

<br />

### Example output:

```json
[
    {
        "time": 1617019313.8090487,
        "messageId": "8b7f3eba-81b0-11eb-97e5-655df6aeb2ec",
        "replyId": null,
        "username": "best_user",
        "nickname": "best_nickname",
        "type": "text",
        "message": "WW91IGhhdmUgbm8gbGlmZSEgWW91IGhhdmUgbm8gam9iLiBZb3UncmUgYmFyZWx5IGEgYmVlIQ==",
        "fileId": null,
        "filename": null
    }
]
```


Sending messages
----------------

<br />
<br />
<br />
<br />









files
=====
Uploading a file to a chatroom
------------------------------
This method allows the user to upload a file to the chatroom.

### Endpoints:
* POST: `http(s)://url:port/api/v0/file/<chatroomId>`
    `<chatroomId>` should be replaced by the ID of the chatroom

<br />


### Required fields:
* username
* filename
    - this is the original name of the file being sent.
    - It will be stored for the recieving client to save the file.
* data


<br />


### Implementation details:
The server only accepts requests that are less than 1mb in size. For this reason larger files have to be split into chunks, that will be individually uploaded. On the last chuk the client will have to set the variable `last` to `true` so the server can finalize the upload. A file will only appear in the messages stream when it has been finalized. Finalized files can no longer be written to by anyone.
**Note**: The chunk size includes the overhead from encoding and/or encryption


<br />

### code example

```py
import os

url = <server url> + "/api/v0/file/" + chatroomId
filename = "cool_picture.png"


# get length of file
length = os.path.getsize(filename)

# Calculate chunk size, allowing for the overhead of base64 encoding
chunk_size = int((1048576*3)/4) -1

# open the file
f = open(filepath, "rb")



# start a loop of sending file chunks
# TODO: finish the notes
last = False
while not last:
        c = f.read(chunk_size)


        # check if this will be the last part
        if len(c) < chunk_size or f.tell() >= length:
            last = True


        data = {
                "username" : globals()['username'],
                "filename" : filename, 
                "fileId"   : fileId,
                "type"     : 'file',
                "last"     : last,
                "data"     : encode_binary(c),
                "kId"      : None
                }


        # make request
        response = globals()['s'].post(url, json=data)
        if response.status_code != 200:
            break
        else:
            print("text")
            print(response.text)
            fileId = response.json().get('fileId')
            print("fileID")
            print(fileId)

    f.close()
    # return the response if the loop stopped
    return response.text, response.status_code

```

Downoading a file from the server
---------------------------------
Method allows you to download a file from the server


### Endpoints:
* POST: `http(s)://url:port/api/v0/file/<chatroomId>`
    `<chatroomId>` should be replaced by the ID of the chatroom





<!--  The maximum amount of data in one request is 1 megabyte, so files that are larger than this have to be uploaded in chunks, broken into multiple requests -->
Below this lies the unchecked and potentially harmful land of outdated documentation
=======================================================================================

chatrooms
=========
Creating a new chatroom
-----------------------
Method should create a new chatroom. Chatrooms are in effect their own segregated server-like systems([check out the docs](https://github.com/tHoMaStHeThErMoNuClEaRbOmB/teahaz-server/edit/new-backend-structure/docs)), which means the user creating a chatroom will have to send all details for registering.
<br />

### chat defaults:
* require_email is on
* Creator becomes chatroom admin
<br />

### endpoints:
* POST: `http(s)://url:port/api/v0/chatroom/`
<br />

### required fields:
* username
* email ( the server owner can change whether the chatroom owner needs an email or not )
* nickname
* password
* chatroom_name ( this is not equivalent to the ID, which will be assigned at random )
<br />

### code example:
```py
url = http:/<server url>/api/v0/chatroom/"

# format required data in json format
data = {
        "username"      : "me",
        "email"         : "me@email.com",
        "nickname"      : "not_me:)",
        "password"      : "password123",
        "chatroom_name" : "best chatroom ever"
        }

# make post request. NOTE: data is sent in the json field 
res = session_obj.post(url=url, json=data)

print(res.text)
```

### example output:
Server returns the ID of the chatroom created

**NOTE**: Due to python being slow at cryptographic operations, this might take a few seconds.
```json
{
  "chatroom": "8b7f3eba-81b0-11eb-97e5-655df6aeb2ec", 
  "name": "best chatroom ever"
}
```







invites
=======
Creating an invite
------------------
Creating an invite so other people can join your chatroom
**NOTE:** On default settings the creator of the invite, has to be admin on the server
<br />

### endpoints:
* GET: `http(s)://url:port/api/v0/invite/<chatroomId>`<br />
`<chatroomId>` should be replaced by the ID of the chatroom
<br />

### required fields:
* username
* expr_time
    - Expiration time of the invite.
    - This has to be a date in Epoch time format.
    - if you dont want the invite to expire then set this to 0.
* uses
    - The number of users that can join with this link.
    - There is no option for unlimited, however there is no upper limit.
<br />


### code example:
```py
import time
url = http(s)://url:port/api/v0/invite/" + chatroomId

data = {
        "username": username,
        "expr_time": str(time.time() + 60 * 60 * 24),
        "uses": str(10)
        }

#NOTE: In GET requests data has to be sent in the http header
res = session_obj.get(url=url, headers=data)

print(res.text)
```
<br />

### example output:
Returns the ID of the invite
```json
"1ffc7d5e-7c2b-11eb-87af-b5145ad18bcb"
```
**NOTE:** This is probably best returned to the user as `chatroomID/inviteId`
(**ps**: I will probably change this to an object with `name`, `chatroom` and `inviteID`. Its staying like this bc I only came up with the idea while writing the docs and I dont have energy rn)
<br />
<br />

Using an invite
---------------
Using that invite you found on a shady website.<br />
(/s Please dont use our project for anything illegal.)<br />
Chatrooms are in effect their own segregated server-like systems([check out the docs](https://github.com/tHoMaStHeThErMoNuClEaRbOmB/teahaz-server/edit/new-backend-structure/docs)), which means that when using an Invite you have to send all details for registering


### endpoints:
* POST: `http(s)://url:port/api/v0/invite/<chatroomId>`<br />
`<chatroomId>` should be replaced by the ID of the chatroom
<br />


### required fields:
* username
* email ( the server owner can change whether the chatroom owner needs an email or not )
* nickname
* password
* inviteID
   - the same invite ID that appeared in section [Creating an invite](#creating-an-invite)
<br />


### code example:
```py
url = http://<teahouse server>/api/v0/invite/" + chatroomId

data = {
        "username"      : "me",
        "email"         : "me@email.com",
        "nickname"      : "not_me:)",
        "password"      : "password123",
        "inviteID"      : "1ffc7d5e-7c2b-11eb-87af-b5145ad18bcb"
        }

# make post request with data in the json field
res = session_obj.post(url=url, json=data)
print(res.text)
```


### example output
returns a json object with the chatroom name and ID
```json
{
    "name": "best chat ever",
    "chatroom": "47aec55e-7c27-11eb-87af-b5145ad18bcb"
}
```
-->
