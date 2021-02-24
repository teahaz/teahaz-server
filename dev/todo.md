general
=======
[ ] get server configs

[ ] get user configs
    - nickname
    - global user colours

[ ] message ids -- some sort of unique id for every message
    * will help with
    - reactions
    - replies
    - deleting, editing?


[ ] reactions

[ ] proper chatrooms
    - list of users with access
    - some settings
    - per user colours
    - themes?

[ ] multiple chatrooms

[ ] user avatars?

[ ] add meaning or id number ot error messges sent back to client

[ ] remove [cookie time] from `init_main_db`



auth
====

cookies
-------

[ ] cookie lifetimes
        - currently cookies have an infinate lifetime.
        - this should be changed by storing an end date alongside the cookie in the database
        - also should probably include this same expiration date as a max_age header so browsers will understand it automatically

[ ] cookie storage
        - currently there is a default/placeholder cookie set bc the server crashes otherwise
        - either this should be removed and fixed, or in worst case check if the cookie sent by user is not the default/placeholder one



databases
=========
[ in progress ] validating chatroom ids
    chatroom id is just a uuid and is not encoded by default
    it makes a lot more sense not to encoded because its a folder on disk
    but this opens it up for some attacks. and for this reasont the following rules have to be true:

    * when a new chatroom is created, the id MUST NOT be user supplied and HAS to be supplied by the server [ as number or uuid]
    * chatroom ids HAVE to be validated very carefully
        - they have to be valid uuids
        - they have to exist on disk
        - cannot contain any / or ..

    NOTE: conv1 is a terrible example of a chatroom id

    * validation is commented in `security.sanitize_chatroom_id`


files
=====
[] make sure server fails if client sends non-encoded files






code review
===========
[] dbhandler



chats
=====
[✓] save chats the user inside the users table in main.db

[✓] add get method for user to see chats that (s)he is in

[✓] make getchats display both the chatroom name and the id

[✓] make error for chatroom does not exists (currently its internal server error)

[✓] make person who created the chatroom admin by default (and member)

[] create method to remove a user from a chatroom 

[] create method to remove chatroom from main.db

[] create a check-chatrooms method that loops though all chatrooms of a user, and makes sure that they exist both in main.db and on disk
    - if its missing from either then delete it from user disk and main.db

[] create invites

[] make dbhandler.checkaccess finally do something

[] error check the shit out of everything


[] make sure the chats work

[] fix conv1, its probably not registered in main.db
