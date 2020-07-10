#this is probably a bad idea but her you go, databaase in json
import json
import bcrypt


def verify(username_and_password):
    # username and password will be seperated by space
    username_and_password = username_and_password.decode("utf-8")
    username = username_and_password[0]
    password = username_and_password[1]


    #need to ge a method to check them
    #if bcrypt.checkpw(password, hashed_password) and bcrypt.checkpw(username, hashed_username):
    # the idea would be to check thse at once so that you cant know if the passowrd or the username is wrong
        # yes this actually makes it more secure





#IMPORTANT this is not a register function, and just blindly adds users
# for security i might need to make it only callable in this file if that is possible in python
# if not then turn this into a register function we will see
def adduser(username, password):
    #needed to be encoded for bcrypt
    # im not sure were this will be used but i think in the end we should not decode this from the message sent by user if possible to avoid decoding and encoding unecessairly
    username = username.encode("utf-8");
    password = password.encode("utf-8");


    # the username and password shoudl be hashed,
    # we do not need the username to be stored normally as each message will start with that
        # you might ask, what is the point of a username, why not just use one id
        # well if two users accidenally use the same id, then they could log into one anothers
        # we can check if the same username exists at registration
            # if we check ids, and it says that it exists then you can just log in as that person
    hashed_username = bcrypt.hashpw(username, bcrypt.gensalt())
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())


    ### some tests
    #print(hashed_username)
    #print(hashed_password)
    #if bcrypt.checkpw(password, hashed_password) and bcrypt.checkpw(username, hashed_username):
    #    print("It Matches!")
    #else:
    #    print("It Does not Match :(")
    #### end of test

    #as usual i will do line by line json
    # is this a good idea?
        # im really not sure
    # does it let me process the data line by line so i dont have to load the whole file in memeory to check it.
        # yes
        # also this might not be as important here as in the message_history, but it works and makes it consistant
    tobestored = json.dumps({"username" : hashed_username.decode("utf-8"), "password" : hashed_password.decode("utf-8") })
    f = open("./thisisnotadatabase", "a")
    f.write(f"{tobestored}\n")

    ###some tests
    #print(tobestored)
    #a = json.loads(tobestored)
    #uname = a["username"].encode("utf-8")
    #passwd = a["password"].encode("utf-8")
    #print(uname)
    #print(passwd)
    #if bcrypt.checkpw(password, passwd) and bcrypt.checkpw(username, uname):
    #    print("It Matches!")
    #else:
    #    print("It Does not Match :(")
    #### end of tests


    



    
    


adduser("yet another username", "with a very special password at that")
