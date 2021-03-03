Welcome to the long overdue documentation of this abomination that I call a rest API :)

docs of /api/v0
==============

## Table of Contents
1. [/message/](#messages)
2. [/file/](#files)
3. [/chatroom/](#chatrooms)
3. [/invites/](#invites)




messages
========



files
=====



chatrooms
=========
GET
---

#### Description:
Returns all chatrooms that your user has access to.



#### code example:
```py
url = http:/<server url>/api/v0/chatroom/"

a = {
        "username": username,
        }


print(res.text)
```


#### return data
```
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








invites
=======



A chatroom admin can get this endpoint to create an Invite. A user 

