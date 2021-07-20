API documentation v0
====================
This Documentation is a brief overview of how each method works, and how a client would interact with them. The documentation tries to be programing language independant but for the most part is written with python and javascript in mind.


Table of contents
-----------------

### Methods
* chatroom
    - creating a chatroom









Documentation of different methods.
==================================



Creating a chatroom.
--------------------
method: `get`
path: `/api/v0/chatroom`

In order to create a chatroom the server needs 3 pieces of information. The name of the chatroom and login details (ie username and password). The login details are needed regardless of whether or not you are already registered ot a differnt chatroom as teahaz has an independant database for all chatrooms. (More docs on this design choice later)

Note: you can also optionally pass a 'nickname' (display name) value to the server. If you dont set this it will automatically be the same as your username.
<br />

example data for this method:
```js
{
    chatroom_name: "chatroom for only cool people",
    username: "one such cool person",
    password: "very secret"
}
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
Channels on teahaz are similar to channels on discord as in they are sperate streams of messages, athat can have independant permissions for different groups of people.


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















