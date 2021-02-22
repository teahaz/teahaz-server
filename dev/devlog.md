devlog
======
this is a document written mostly for myself.
ill write here whenever the fuck it pleases me
usually something about what im working on, what i recently finished, or random thoughts that are important (maybe)

#22 feb 2021
## multi-chatroom support
idea is that chatrooms are saved by uuid as a folder, but this is not very user friendly. My solution to this is to rename users.db to main.db and have a chatrooms table in it. The chatrooms table would store the chatroomID the chatroom name, and maybe the occupance/admin (but the users of the chatroom should most likely be in the db inside the chatroom)


# 14 feb 2021
## docker
for the past days i have been working on making docker work nicely on the server
some important features of this are:
* server runs with out any dependancies, other than docker
* server setup is one command: `sudo ./run`
* server can auto git pull updates

this is not done yet, just havent wrote in here for a while so i thought i might
currently the main issue is that the server just errors and moves on when git pull fails. I want the server to shutdown in this case. So far the best way i have found to do this is to somehow use the healthcheck feature of docker



# 01 feb 2021
## cleanup
i have added a lot of new code in the past month or so and the codebase has become a huge mess. I think its about time to spend some time on cleanup

### errors
one of the biggest problems are errors
errors are completely differnet on all files. they are also most often not logged, and even where they are logged they dont often folow the standard

#####  this should be a priority to fix



# 31 jan 2021

## username vs userId
this refers back to an entry with the same name on jan 30

userid should be either username or email depending on server settings
for more lax servers it could be just a username, but if a server wants to verify all its users then it has to be and email address
i want to implement it so that even if there is an email given the username is still present so users can find eachothers permanent names 
it should be the users choice whether he/she logs in with a username or a password

##### both the username and the email should be checked for duplicats before registering

# 30 jan 2021
## logs
currently logs are an utter mess
the main problem is that some logs try provide inforamtion for ppl testing the server, and yet other logs seem production ready
my current plan is to do more dev-friendly logs, and later i can re-write all to make more sense for the production ready server


## username vs userId
this refers back to an entry with the same name on jan 23
the status now is as described in the previous entry, there is a userId that doesnt change, and a nickname that can be changed at any time
this raises one big issue: how does the user log in?

to put it simply we cannot use the nickname for logging in, but we also cannot expect a user to memorize their userId
we need something in the middle, most platforms use an email address

my idea is to have a nickname and an unchangable username/email

#### username or email
###### username
pros:
* privacy

###### email
pros:
* could make a verification system to avoid people having thousands of alt accounts
* emails change rarely and users are very likely to remember them
* emails are unique and we wont have internal collisions (obviously would still need to check tho)
* emails being unique avoid cross-server collisions


for now i will jsut have a userId string that could be anything, but should be refered to as email for the most part




# 23 jan 2021
## working with cookies
im going to try and implement the 2nd idea for the users database

## username vs userid
a new thing that i have come up with is to replace username with userid intermally
infact there will no longer be a username but rather just a nickname to represent that it has no real value

the userid will not be shown to the end user, but it will be what the server uses for client server communication, authentication, and literarly everything else

if possible ill try make it so that other ppl can never find your userid, this might not be very easy tho and is not high on my list of priorities

on that note i will cut cookies in half again to replace everythign i have done so far with userID instead of username


## removed master passord
as it stands now the master passowrd was not being used and just made the whole main.py file feel messy
i have this code here bc i think the idea was alright and later when we actually need the password then ill be happy not to have to re-write it
    ##!!!!!!!!! important:
    ## everything the server relies heavily on this master password, and it must be kept really well guarded
    #    # if the master password is leaked then everyone is compromised
    #    # maybe i should implement some sort of 2fa
    ## the key needs to be accessed everywhere on the server
    #    # i may in future restrict this so only a few functions can access it
    #global master_key

    ## check if TEAHAZ_MASTER_KEY enviroment variable exists
    #if not "TEAHAZ_MASTER_KEY" in environ:
    #    # if it doesnt then ask for password
    #    print("please give master password, or insert authentication key")
    #    master_key = input(":: ")
    #    # set variable, because flask often restarts and we dont want to type the password in each time
    #    environ["TEAHAZ_MASTER_KEY"] = master_key
    #else:
    #    # if it exists then just get it
    #    master_key = environ["TEAHAZ_MASTER_KEY"]



# 22 jan 2021
## working on cookies
new idea for cookies
the former idea i had for cookies would be really slow, as well as would have the potential of exposing the master password
also it seemed like re-inventing jwt tokens
so, although i dont like it, i think im going to go for good old session cookies
i think i will also add a users.db 
2 main ideas for users.db
* 1
    id = cookie
    this would mean that each entry in the db would have an id that is the cookie of the user
    a user could have more then one entry, if they have more then one device.
    entry would store a small amount of information, probably just `<id/cookie, user id>`
    pros:
        probably faster than the other one

* 2
    id = user id
    in this implementation each entry would have the users unique id, along with all cookies connecting to them
    this could store more information, including all user specific data, like colour, avatar, password(hash), nickname, etc
    pros:
        all the data in one place
        makes it easier to manage





# 19 jan 2021
## working on cookies
idea is that we should not store cookies, but have hashes, that the server can verify
this would look something like a jwt token, except the user would not be able to decode it
the cookie would be a hash of the users (something: username, id, password) and the master passowrd of the server

## master passwod
the server relies heavily relies/will rely heavily on the master password
    i dont think there is a sain better way to do this, other then offer an option for multiple passwords
that said we need a way for the master password to be secure, im thinking of adding some measure of 2fa into it.
so far ideas of 2fa (this would mean that anywhere the master password is hashed with <_2favalue> before it is used anywhere):
    some hwid
    some file on the server, outside of the server directory

also maybe such a 2fa hash should be used as some sort of salt, so if masterpassword is leaked from some other function it cannot actually use it until it leaks the 2fa key





# 18 jan 2021
with the project being about 4 months old, maybe its a bit late to stat a devlog, 
but i guess better late then never
i took about a month long break, and i have no idea what i was working on
apparently the server has a master password now

