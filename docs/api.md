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
Getting messages by messageId
-----------------------------
This method should return one messasge, with the messageId that the client supplied



### Endpoints:
* GET: `http(s)://url:port/api/v0/messasge/<chatroomId>`
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

<br />
<br />


Getting all messages since \<time\>
---------------------------------
This method should return all messages in a chatroom that were sent since the time variable. The time variable should be in epoch/unix time.

### Endpoints:
* GET: `http(s)://url:port/api/v0/messasge/<chatroomId>`
`<chatroomId>` should be replaced by the ID of the chatroom
<br />


### Required fields:
* username
* chatroomId
* time

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
<br />
<br />
<br />
<br />
<br />
<br />
<br />


Below this lies the unchecked and potentially harmful land of outdated documentation
=======================================================================================



files
=====
### endpoints:
* GET: `http(s)://url:port/api/v0/file/<chatroomId>`<br />
`<chatroomId>` should be replaced by the ID of the chatroom
<br />

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
