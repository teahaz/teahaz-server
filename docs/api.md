Welcome to the long overdue documentation of this abomination that I call a rest API :)

docs of /api/v0
==============

## Table of Contents
1. [/message/](#messages)
2. [/file/](#files)
3. [/chatroom/](#chatrooms)
    - [creating-a-new-chatrom](#Checking-chatrooms-you-have-access-to)
5. [/invites/](#invites)




messages
========



files
=====



chatrooms
=========
Checking chatrooms you have access to
-------------------------------------
A GET request to /chatroom/ should return all chatrooms that your user has access to

#### required fields
* username


#### code example:
```py
url = http:/<server url>/api/v0/chatroom/"

data = {
        "username": username,
        }

#NOTE: In GET requests data has to be sent in the http header
res = requests.get(url=url, headers=data)

print(res.text)
```



#### example return data:
Server returns both the name and the ID of every chatroom the user is in
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


Creating a new chatroom
-----------------------
Sending a POST request to /chatroom/ should create a new chatroom. The creator of the chatroom will automatically be added as an admin.

#### required fields
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
res = requests.post(url=url, json=data)

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



A chatroom admin can get this endpoint to create an Invite. A user 

