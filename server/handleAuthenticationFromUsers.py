#this is probably a bad idea but her you go, databaase in json
import json
import bcrypt


def verify(username_and_password):
    # username and password will be seperated by space
    print(len(username_and_password))
    username_and_password = username_and_password.decode("utf-8")
    
    

    username_and_password = username_and_password.split(" ")
    username = username_and_password[0]
    password = username_and_password[1]



    #need to ge a method to check them
    #if bcrypt.checkpw(password, hashed_password) and bcrypt.checkpw(username, hashed_username):
    # the idea would be to check thse at once so that you cant know if the passowrd or the username is wrong
        # yes this actually makes it more secure



    # read the userlist on by one to check them
    # this should load the whole thing into memory, but that should not be an issue as users dont set good passwords and it wont take much memory
        # remind me to change this if we have over 2 million users on this one server
    with open("./thisisnotadatabase", "r")as plsdontjudgemydb:
        db = plsdontjudgemydb.readlines()
        for entry in db:
            entry = json.loads(entry)
            
            



            # bcrypt will return True if the its a match, so this will be true if both the username and the password match
            # IMPORTANT you need to check these at the same time for obvious security
            if bcrypt.checkpw(username.encode("utf-8"), entry['username'].encode('utf-8')) and bcrypt.checkpw(password.encode("utf-8"), entry['password'].encode("utf-8")):  

                # add, [if needed] any code to deal with the correct password
                print("username and password accepted")

                return True
    
    print("username and password unacceptable")
    return False


    



# ony really for internal use
def hashpassword(password):
    import hashlib
    import base64

    m = hashlib.sha256()
    m.update(password.encode("utf-8"))
    hashed_password = base64.b64encode(m.digest())

    return hashed_password.decode("utf-8")




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

    


# WARNING this is a temporary solution untill i dont have a register function
# by calling the program as main, you run the add user method
# this will be ripped out later so pls dont rely on it

if __name__ == "__main__":
    print("add user directly")
    print("WARNING: this is only temporary")
    print("this next bit alows you to add a user to the 'database'[ which it totally isnt, but idk how to refer to it]")
    username = str(input("username: "))

    password = str(input("password: "))
    password = hashpassword(password) 
    print(password)

    choice = input("\n\n do you want to [V]erify and existing user or [A]dd a new one? [V/A]: ")
    if choice == "V":
        print("so you have chosen verify")
        verify(f"{username} {password}".encode("utf-8"))
    else:
        print("so you have chosen adduser")
        adduser(username, password)

