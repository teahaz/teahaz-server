API documentation v0
====================
This Documentation is a brief overview of how each method works, and how a client would interact with them. The documentation tries to be programing language indipendant but for the most part is written with python and javascript in mind.


Table of contents
-----------------

### Methods
* chatroom
    - creating a chatroom
    - get chatroom information / check login
* login
    - login
* channels
    - create channel
* messages
    - send message
    - send reply message








Documentation of different methods.
==================================



Creating a chatroom.
--------------------
method: `post`
path: `/api/v0/chatroom`

In order to create a chatroom the server needs 3 pieces of information. The name of the chatroom and login details (username and password). The login details are needed regardless of whether or not you are already registered ot a differnt chatroom as teahaz has an independent database for all chatrooms. (More docs on this design choice later)

Note: you can also optionally pass a 'nickname' (display name) value to the server. If you dont set this it will automatically be the same as your username.
<br />

example python code for creating a chatroom
```python
import requests

data = {
    "chatroom_name": "th dev"
    "username": YOUR_USERNAME,
    "password": YOUR_PASSWORD
}

r = requests.post(url="http://teahaz.co.uk/api/v0/chatroom/", data=data)

print(r.json())
```

<br />
<br />

The server will set up a new [mongodb database](https://docs.mongodb.com/manual/core/databases-and-collections/) for the chatroom, with 5 collections: users, messages, channels, classes, and chatroom. (more detail on these later). The server also adds some default information into these collections:
- adding the creator of the chatroom (constructor in teahaz terms) to the users collection
- creating a 'default' channel
- creating the 'constructor' (reserved only for the creator of a chatroom) and 'default' (for everyone) classes and adding your user to both.
- adding an event into the messages collection to to notify people of a new user (in the case of the first user this doesnt have much meaning)


<br />
<br />

Example return data for creating a chatroom:
```js
{
  channels: [
    {
      channelID: '8aa869a0-e8ec-11eb-9db0-b42e99435986',
      name: 'default',
      permissions:
      [
          {
              classID: '1',
              r: true,
              w: true,
              x: false
          }
      ]
    }
  ],
  chatroomID: '8aa5f076-e8ec-11eb-9db0-b42e99435986',
  classes: [
    {
        classID: '0',
        name: 'constructor'
    },
    {
        classID: '1',
        name: 'default'
    }
  ],
  settings: [
    {
        sname: 'chatroom_name',
        svalue: 'chatroom for only cool people',
        stype: 'string'
    },
    {
        sname: 'min_password_length',
        svalue: 10,
        stype: 'int'
    },
    {
      sname: 'default_channel',
      svalue: '8aa869a0-e8ec-11eb-9db0-b42e99435986',
      stype: 'string'
    }
  ],
  users: [
    {
      classes:
      [
          '0',
          '1'
      ],
      colour:
      {
          b: null,
          g: null,
          r: null
      },
      username: 'one such cool person',
      nickname: 'one such cool person'
    }
  ]
}
```

As you can probably see wherever possible the server tries to return as much information as it can. This is done as an attempt to help the user of the api not have to make as many requests. You can read more on what this data means [here](https://http.cat/501).

<br />
<br />
<br />

Login
-----
method `post`
path: `/api/v0/login/`[\<chatroomID\>](https://http.cat/501)

<br />

If the chatroom already exists, and your user has already joined by some means, it can now use the login method. The method for the most part is pretty much what you would expect, you need to send your username and password and you will recieve a cookie so that you can use to further communicate with the server.

Example python code to login:
```py
import requests

chatroomID = ID_OF_CHATROOM

data = {
    "username": YOUR_USERNAME,
    "password": YOUR_PASSWORD
}

r = requests.post(url="http://teahaz.co.uk/api/v0/login/"+chatroomID, data=data)

print(r.json())
```

<br />

If successful the server will assign you a new cookie, and return the [standard data for joining a chatroom](http://http.cat/501).

<br />
<br />

get chatroom information / check login
--------------------------------------
method `get`
path: `/api/v0/chatroom/`[\<chatroomID\>](https://http.cat/501)

This method serves 2 main purposes:
1. Getting up-to-date information about a chatroom.
2. Checking if the client is logged in.

In order to make the request you need to send your username and a cookie.

Example python code:
```
import requests

chatroomID = ID_OF_CHATROOM

data = {
    "username": YOUR_USERNAME,
}

r = requests.get(url="http://teahaz.co.uk/api/v0/chatroom/"+chatroomID, headers=data)

print(r.json())
```
**Note**: Data has to be sent in the http header. [why?](https://http.cat/501)

If you are logged in then the method returns the [standard data for a chatroom](http://http.cat/501). If however you are not logged in, this along with most functions that require a login will return "client not logged in" with a status code of 401.



<br />
<br />

Create channel
--------------
method `post`
path: `/api/v0/channels/`[\<chatroomID\>](https://http.cat/501)

Channels on the server are like seperate streams of messages similar to what discord and other larger group messaging platforms have. To create a new chatroom you need to send the server your username, the name of the new chatroom and some permission information so the server knows who can view, write, or edit the channel.

Permission information is stored as a list. The list needs to have a classID that refers to a class of users, and it needs to have an r, w and x value for read write and manage. (This scheme is taken from unix systems where x is execute, but as that doesnt make much sense here we have changed it to manage.)

Example permissions for a channel:
```js
[
    {
        classID: "i",
        r: true,
        w: true,
        x: false
    },
    {
        classID: "cc2b9f4c-eef9-11eb-b1eb-b42e99435986",
        r: true,
        w: true,
        x: true
    }
]
```
NOTE: classID in most cases in a UUID, classID: "1" refers to the default class (everyone).

<br />

Example python code for creating a new channel:
```py
import requests

chatroomID = ID_OF_CHATROOM

data = {
    "username": YOUR_USERNAME,
    "channel-name": NAME_OF_NEW_CHANNEL,
    "permissions": [
        {
            classID: "i",
            r: true,
            w: true,
            x: false
        },
        {
            classID: "cc2b9f4c-eef9-11eb-b1eb-b42e99435986",
            r: true,
            w: true,
            x: true
        }
    ]
}

r = requests.post(url="http://teahaz.co.uk/api/v0/chatroom/"+chatroomID, data=data)

print(r.json())
```

If successful the server should return the ID, name, and permissions of the new channel.

Example:
```
{
  channelID: 'cc2b9f4c-eef9-11eb-b1eb-b42e99435986',
  name: 'default',
  permissions: [ { classID: '1', r: true, w: true, x: false } ]
},
```

<br />
<br />



send message
------------
method: `post`
path: `/api/v0/message/`[\<chatroomID\>](https://http.cat/501)

This method lets you send a message to a teahaz chatroom. To send a message you need to specify 2 things, the ID of the channel you are sending the meessage to and the message itself. In teahaz each chatroom has multiple channels (seperate streams of messages), and a message sent by a user can only belong in one channel. For this reason you must specify a valid channelID in each message.

Currently teahaz clients dont support end to end encryption (**yet**), even though on the server-side most of the infrastructure for it is already built out. As a placeholder all clients must base64 encode messages that are being sent to the server.


Example python code for sending a message:
```py
import base64
import requests


chatroomID = ID_OF_CHATROOM
message_text = "Hello, how are you guys?"

data = {
    channelID: ID_OF_CHANNEL,
            # base64 encoding the message
    message: base64.b64encode(message_text.encode('utf-8')).decode('utf-8')
}

r = requests.post(url='http://teahaz.co.uk/api/v0/messages/'+channelID, data=data)

print(r.json())
```

The server should return your message in the same format as a standard request to get messages does.

Example returned data:

```js
{
  messageID: 'd334da3e-f3c1-11eb-b9fe-4f5968c71063',
  time: 1627929936.2626493,
  channelID: 'cdf68efa-f3c1-11eb-b9fe-4f5968c71063',
  username: 'a',
  type: 'text',
  data: 'SGVsbG8sIGhvdyBhcmUgeW91IGd1eXM/',
}
```
More information on how to interpret this [here](https://http.cat/501)


**NOTE**: When displaying the message on a client, you should not display the users `username` but rather get their `nickname`(display name) from previously got user data.


Note for people making client files: `teahaz.js` adds the following information to each message to make the consumers work easier, I highly recomend doing this too.
```
  message: 'hello',
  colour: { r: null, g: null, b: null },
  nickname: 'a'
```




<br />
<br />



send reply message
------------------
Sending a message reply is largely the same as sending a standard message, other than a few key differences:

- You need to specify a `replyID`. This ID should be the messageID of an existing message.
- The message `type` has to be `reply-text`

The returned data should reflect these differences as well.




<br />
<br />




get messages
------------
method: `get`
path: `/api/v0/message/`[\<chatroomID\>](https://http.cat/501)

Download messages from a server.
Currently there is only one way to do this. You must specify a time , and the server will return all messages that have been sent since then.


**Note:** yes, this could overload the server if there are too many messages. yes, I have thought of this, but currently I dont have a better idea for a get method, and ill implement one when I do. Also for now there is no rate limit. :/

<br/>

By default get looks for new messages in every channel that your user has read access to, and will also get system messages that dont belong to any channel. You can change this by sending a channelID, in which-case the server will only return messages in that channel and system messages.


Example python code:
```py
import requests

chatroomID = ID_OF_CHATROOM

headers = {
    "username": YOUR_USERNAME,
    "channelID": ID_OF_CHANNEL, # (optional)
    "time": TIME_IN_EPOCH_FORMAT
}

r = requests.get(url="http://teahaz.co.uk/api/v0/messages/"+chatroomID, headers=headers)

print(r.json())

```
**Note**: Data has to be sent in the http header. [why?](https://http.cat/501)



Example returned data:
```
[
  {
    messageID: 'ec22d058-fb9d-11eb-9930-91dece58809e',
    time: 1628794125.5074627,
    type: 'system',
    data: {
      event_type: 'newuser',
      user_info: {
        username: 'a',
        nickname: 'a',
        colour: { r: null, g: null, b: null },
        classes: [ '0', '1' ]
      }
    }
  },
  {
    messageID: 'eec2a338-fb9d-11eb-9930-91dece58809e',
    time: 1628794129.9102864,
    channelID: 'e9840327-fb9d-11eb-9930-91dece58809e',
    username: 'a',
    type: 'text',
    data: 'aGVsbG8='
  }
]
```
The above example has a system message and a message sent by a user called `a`. Messages on th can take many differnt forms, for more information refer to [this](http://http.cat/501).



**NOTE**: When displaying the message on a client, you should not display the users `username` but rather get their `nickname`(display name) from previously got user data.


Note for people making client files: `teahaz.js` adds the following information to each message to make the consumers work easier, I highly recomend doing this too.
```
  message: 'hello',
  colour: { r: null, g: null, b: null },
  nickname: 'a'
```
<br />
<br />




Create an invite
----------------
method: `get`
path: `/api/v0/invites/`[\<chatroomID\>](https://http.cat/501)

The only way to add a new person to a chatroom is through an invite. This method shows how a \**chatroom admin* can create an inivte.

*chatroom admin*: Currently only users with a role that has the `admin` attribute set to true can create an invite. This will later change as more granular permissions are introduced.



**Arguments:**
- uses: The amount of times an invite can be used before it expires.
- expiration\_time: Epoch date, represents when the invite expires.
 For these first 2 there is no option for unlimited, but you can set very large numbers for both, in affect making them unlimited.
- classes: An array of classID's that anyone using the invite will get assigned to. (optional, default is ['1'])

<br />
<br />

### An issue with the current implementation
Http headers dont natively support arrays. On the other hand classes has to be an array. The server currently supports 2 methods of getting around this.

1. The proper method:
Http has a built in way of getting around this, and that is to just set multiple headers to the same thing. For example:
```js
classes: <uuid>
classes: <uuid>
classes: 0
```
This unfortunately isnt that simple in most programming languages, as json doesnt allow you to declear the same key twice.


2. The very unclean way:
Teahaz server will understand and interpret a string of values seperated by commas the same way.
For example:
```
classes: 1, 2, 3, 4, 5, 6, 7, 8
```


Example python code for creating an invite:
```py
import requests

chatroomID = ID_OF_CHATROOM

headers = {
    "username": YOUR_USERNAME,
    "channelID": ID_OF_CHANNEL, # (optional)

    "uses": NUMBER_OF_USES,
    "expiration_time": TIME_IN_EPOCH_FORMAT,
    "classes": str(['0', UUID, UUID, UUID]).strip('[').strip(']')
}

r = requests.get(url="http://teahaz.co.uk/api/v0/invites/"+chatroomID, headers=headers)

print(r.json())
```


Example return:
```js
{
  inviteID: '472c23c0-0650-11ec-8015-b42e99435986',
  username: 'a',
  uses: '1',
  classes: ['0', UUID, UUID, UUID],
  expiration_time: '1629971240.268'
}
```





<br />
<br />
<br />
<br />
<br />
<br />
<br />
<br />












old docs:
=========

Table of contents
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
Channels on teahaz are similar to channels on discord as in they are sperate streams of messages, athat can have independent permissions for different groups of people.


Example of a channel object:

```js
[
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
]
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


### uses
type: int
A variable used with invites. This specifies how many times an invite can be used. If it is equal to 0 then the invite is expired.
It is also decremented by one every time someone uses the invite.


### expiration-time
type: float (epoch time)
This date represents when an invite expires. Invites cannot be used after their expiration time has passed.


## settings
type: array of objects (list of dicts)
Chatroom settings are stored as a list of objects because they will often change and this way a client can dynamically display them instead of issueing updates all the time.

#### sname
Represents the name (title) of a setting.

#### svalue
Value that the setting is set to.

#### stype
Data type of the setting, this can help clients automatically validate inputs. Also allows clients to automatically use toggles for boolian values.


<br />
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

* 200:
OK
* 400:
user error
* 401:
not logged in
* 403:
Permission denied (usually trying to access something your user does not have permission to)
* 500:
Server error (you did nothing wrong, please report it to me! )

Hopefully I didnt miss anything.

<br />
<br />
<br />


More detail on methods
======================

<br />

## chatroom
url: `/api/v0/chatroom`

### - post
action: Create a new chatroom.
- [x] Method is functional.
- [x] Method is finished.
- [x] Sets cookie 

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


<br />

### - get
action: Get information about a chatroom.
- [ ] Method is functional.
- [ ] Method is finished.
- [ ] Sets cookie 

### - delete
action: Delete a chatroom.
- [ ] Method is functional.
- [ ] Method is finished.
- [ ] Sets cookie 


<br />
<br />

## login
url: `/api/v0/login/<chatroomID>`

### - post
action: Login to a chatroom.
- [x] Method is functional.
- [x] Method is finished.
- [x] Sets cookie 

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


### - get
action: Check if you are logged in.
- [x] Method is functional.
- [x] Method is finished.
- [ ] Sets cookie 



needed data:
```js
    userID: "UUID (str)"
```

There is no useful data returned by this, other than a status code to indicate whether or not you are logged in.

status code 200 == logged in
status code 401 == not logged in

### - delete
action: Delete user account.
- [ ] Method is functional.
- [ ] Method is finished.
- [ ] Sets cookie 



<br />
<br />


## users
url: `/api/v0/users/<chatroomID>`

### - get
action: Get all users of a chatroom
- [x] Method is functional.
- [ ] Method is finished.
- [ ] Sets cookie 

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
### - post
action: Update personal information
- [ ] Method is functional.
- [ ] Method is finished.
- [ ] Sets cookie 


### - put
action: Update some other users information.
- [ ] Method is functional.
- [ ] Method is finished.
- [ ] Sets cookie 


### - delete
action: Kick user.
- [ ] Method is functional.
- [ ] Method is finished.
- [ ] Sets cookie 


<br />
<br />

## channles
url: `/api/v0/channels/<chatroomID>`

### - post
action: Create a new channel
- [x] Method is functional.
- [ ] Method is finished.
- [ ] Sets cookie 


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

### - get
action: Get all channels the user has read access to
- [x] Method is functional.
- [ ] Method is finished.
- [ ] Sets cookie 


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

### - delete
action: Delete a channel.
- [ ] Method is functional.
- [ ] Method is finished.
- [ ] Sets cookie 

<br />
<br />

## messages
url: `/api/v0/messages/<chatroomID>`

### - post
action: send message to chatroom/channel
- [x] Method is functional.
- [ ] Method is finished.
- [ ] Sets cookie 

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

### - get
action: Get message
- [x] Method is functional.
- [ ] Method is finished.
- [ ] Sets cookie 



There are 2 main ways to get messages:
- you can get all messages since \<time\>
- You can get \<count\> number of messages. (optionally with a starting time).

<br/>

1. get since



needed data:
```
    userID: "UUID (str) || '0'",
    get-method: 'since',

    time: float (time.time())

    channelID: "UUID (str)"   (optional)
```


<br/>
<br/>

2. get count
```
    userID: "UUID (str) || '0'",
    get-method: 'count',

    count: int (optional, defaults to 10)
    time: float (time.time()) (optional, defaults to now)

    channelID: "UUID (str)"   (optional)
```

optional arguments:

* channelID
type: "UUID (str)"
If this is set then the server will only look in the specified channel for messages.


### - delete
action: Delete a message.
- [ ] Method is functional.
- [ ] Method is finished.
- [ ] Sets cookie 


### - put
action: Update (edit) a message.
- [ ] Method is functional.
- [ ] Method is finished.
- [ ] Sets cookie 

<br />
<br />

## files
### - get
action: Download a file.
- [ ] Method is functional.
- [ ] Method is finished.
- [ ] Sets cookie 

### - post
action: Upload a file.
- [ ] Method is functional.
- [ ] Method is finished.
- [ ] Sets cookie 


## invites
### - get
action: create an invite
- [x] Method is functional.
- [ ] Method is finished.
- [ ] Sets cookie 


needed data:
```js
    userID: "UUID (str) || '0'",

    uses: int (optional),
    expiration-time: float (time.time()) (optional),
```


example return: 
```js
{
  invite: 'teahaz:d2e46916-dd99-11eb-b37b-b42e99435986/d56323a8-dd99-11eb-91b9-b42e99435986',
  uses: 10,
  'expiration-time': 1626098634.4710624,
  inviteID: 'd56323a8-dd99-11eb-91b9-b42e99435986'
}

```

## - post
action: create an invite
- [x] Method is functional.
- [ ] Method is finished.
- [x] Sets cookie 

needed data:
```js
    inviteID: "UUID" (str)

    username: "string"
    password: "string"
```

example return:
(all information about a chatroom)
```js
{
  userID: 'e9685fc0-dd9a-11eb-8fa6-b42e99435986',
  chatroomID: 'e4d9e74e-dd9a-11eb-9025-b42e99435986',
  chatroom_name: 'conv1',
  channels: [
    {
      channelID: 'e4ddeb1e-dd9a-11eb-9025-b42e99435986',
      channel_name: 'default',
      public: 1
    },
    {
      channelID: 'e6f32f36-dd9a-11eb-8113-b42e99435986',
      channel_name: 'memes channel',
      public: 1
    }
  ],
  settings: [
    { sname: 'chat_name', svalue: 'conv1', stype: 'str' },
    { sname: 'min_password_length', svalue: 10, stype: 'int' }
  ]
}

```

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















