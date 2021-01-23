#devlog
this is a document written mostly for myself. 
ill write here whenever the fuck it pleases me
usually something about what im working on, what i recently finished, or random thoughts that are important (maybe)




# 18 jan 2021
with the project being about 4 months old, maybe its a bit late to stat a devlog, 
but i guess better late then never
i took about a month long break, and i have no idea what i was working on
apparently the server has a master password now



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




# 23 jan 2021
im going to try and implement the 2nd idea for the users database

## username vs userid
a new thing that i have come up with is to replace username with userid intermally
infact there will no longer be a username but rather just a nickname to represent that it has no real value

the userid will not be shown to the end user, but it will be what the server uses for client server communication, authentication, and literarly everything else

if possible ill try make it so that other ppl can never find your userid, this might not be very easy tho and is not high on my list of priorities

on that note i will cut cookies in half again to replace everythign i have done so far with userID instead of username

