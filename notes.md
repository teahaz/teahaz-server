# new teahaz 
old files are in the .old directory

#bazsi

# me
basic server is done, missing auth and encryption, but is soo much more stable then the old server and is soo much cleaner

### methods
###### send
send a message
+ message structure
{
    "username": "name",
    "cookie": "AAAAA",
    "type": "text", 
    "message": "fuck you"
}

- username 
    not going to explain this
- cookie
    not yet implemented
- type
    this could either be text or file
    they all get send in the same way 
- message
    this could be some message or the contents of a file

ofc all messages are base64 encoded
so the send method looks more like this:
{
    "username": "ZnVja2ZhY2U=",
    "cookie": "QUFBQUE=",
    "type": "dGV4dA==",
    "message": "ZnVjayB5b3U="
}


###### get
get all the messages since <time> 
+ message structure
{
        'username': 'fuckface'
        'cookie': 'AAAAA', 
        'last_get_time': "1597017007.553126"
}
- username 
    not going to explain this
- cookie
    not yet implemented
- last get time
    unix time format of when the last get method was called
    or the last message you want to download
    
    this could be just someone wanting to download old messages
    tho it would be nice if these were cashed locally too


