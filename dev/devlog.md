#devlog
this is a document written mostly for myself. 
ill write here whenever the fuck it pleases me
usually something about what im working on, what i recently finished, or random thoughts that are important (maybe)




# jan 18 2021
with the project being about 4 months old, maybe its a bit late to stat a devlog, 
but i guess better late then never
i took about a month long break, and i have no idea what i was working on
apparently the server has a master password now



# jan 19 2021
## working on cookies
idea is that we should not store cookies, but rather get decypher them
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
