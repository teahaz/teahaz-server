Welcome to the long overdue documentation of this abomination that I call a rest API :)

docs of /api/v0
==============

## Table of Contents
1. [/message/](#messages)
2. [/file/](#files)
3. [/chatroom/](#chatrooms)
    - [Checking chatrooms you have access to](#Checking-chatrooms-you-have-access-to)
    - [Creating a new chatroom](#Creating-a-new-chatroom)
5. [/invites/](#invites)
    - [Creating an invite](#Creating-an-invite)
    - [Using an invite](#Using-an-invite)





messages
========



files
=====



chatrooms
=========
Checking chatrooms you have access to
-------------------------------------
A GET request to `/chatroom/` should return all chatrooms that your user has access to

#### required fields:
* username


#### code example:
```py
url = http:/<server url>/api/v0/chatroom/"

data = {
        "username": username,
        }

#NOTE: In GET requests data has to be sent in the http header
res = session_obj.get(url=url, headers=data)

print(res.text)
```



#### example return data:
Server returns both the name and the ID of every chatroom the user is in
```json
[
    {
        "name": "chatroom_name1",
        "chatroom": "77e3d806-7c07-11eb-87af-b5145ad18bcb"
    },
    {
        "name": "chatroom_name1",
        "chatroom": "fd4f0462-7c10-11eb-87af-b5145ad18bcb"
    }
]
```


Creating a new chatroom
-----------------------
Sending a POST request to `/chatroom/` should create a new chatroom. The creator of the chatroom will automatically be added as an admin.

#### required fields:
* username
* chatroom_name
   - chatroom name is the nickname of the chatroom and **not** the ID


#### code example:
```py
url = http:/<server url>/api/v0/chatroom/"

# format required data in json format
data = {
        "username": username,
        "chatroom_name": input("chatroom name: ")
        }

# make post request. NOTE: data is sent in the json field 
res = session_obj.post(url=url, json=data)

print(res.text)
```

#### example output:
Server returns the ID of the chatroom created
```
chatroom_name: best chat ever

"47aec55e-7c27-11eb-87af-b5145ad18bcb"
```







invites
=======
Creating an invite
------------------
Sending a GET request to `/invite/` should create an invite.
**NOTE:** The creator of the invite has to be admin of the chatroom they are creating an invite for!

#### required fields:
* username
* chatroom
    - The chatrooms ID

* expr_time
    - Expiration time of the invite.
    - This has to be a date in Epoch time format.
    - if you dont want the invite to expire then set this to 0.

* uses
    - The number of users that can join with this link.
    - There is no option for unlimited, however there is no upper limit.


#### code example:
```py
import time
url = http://<teahouse server>/api/v0/invite/"

data = {
        "username": username,
        "chatroom": chatroomId,
        "expr_time": str(time.time() + 60 * 60 * 24),
        "uses": str(10)
        }

#NOTE: In GET requests data has to be sent in the http header
res = session_obj.get(url=url, headers=data)

print(res.text)
```

#### example output:
Returns the ID of the invite
```
"1ffc7d5e-7c2b-11eb-87af-b5145ad18bcb"
```


Using an invite
---------------
Sending a POST request to `/invite/` with an invite ID should add your use to the chatroom the invite corresponds to.

#### required fields:
* username
* inviteID
 - the same invite ID that appeared in section [Creating an invite](#creating-an-invite)



#### code example:
```py
url = http://<teahouse server>/api/v0/invite/"

data = {
        "username": username,
        "inviteId": input("invite: ")
        }

# make post request with data in the json field
res = session_obj.post(url=url, json=data)
return res.text
```


#### example output
returns a json object with the chatroom name and ID
```json
{
    "name": "best chat ever",
    "chatroom": "47aec55e-7c27-11eb-87af-b5145ad18bcb"
}
```
