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
[ ] make sure server fails if client sends non-encoded files



code review
===========
this is not really a todo but a list of things i have already done

[done] /login
[done] /register
[done] /message
[done] /file

[ ] everything else

