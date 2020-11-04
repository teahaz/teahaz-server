stop using bransh add_sql
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


<<<<<<< HEAD
            5: this is the path to the saved creds/where they should be saved. (its in json format so dont shout at me)
                if you have password_auth=false it will use creds here to log in
                else it will save creds here
                the username is unencrypted so you can use it instead of `name` in the code

    ### i need to add 2 things to the text above, 
            1: if i said anywhere that autologin doesnt work, then its a lie bc i fixed it (my comments are more bloated then the code lmao)
            2: check out client/testers/authTest.py for a commented example of how to use it

i feel like i need to add an explentaion for my abuse of the json format
    i store data line by line bc this way i can read and process a line without putting the whole file into memory
    this is normal tho i dont know any implementation that uses json with this
    but really why not, python is slow enough this wont make much of a difference, this is a messaging app not a game, that extra ~3ms wont matter
=======
### known bugs
+ storing messages
for storing messages the server uses one file, in general this could be good but has one big issue
if two messages are being sent at once then they might try to write to the file at once which could cause issues
>>>>>>> 22fdcd5666c78190ef890b21b3b698a6c74d9721
