todos
=====
bug fixes
---------

upcoming
--------

- [ ] add kid (Key ID) field to messages



- [ ] method to get a message by its id


- [ ] endpint where a user can check/change their own configs


- [ ] chatroom configs


- [ ] server configs


- [ ] endpoint where the client can get some server configs that it needs to know
    - max request size
    - max stored filesize
    - does creating a chatroom require verified email


- [ ] endpoint to check chatroom configs (and some permissions should be able to change them)
    - maximum text size limit
    - not sure what else yet


- [ ] multiple channels in one chatroom
    - could be implemented entirely in json (ei a channel field)
    - and yes this would still allow you to have permissions, just stored in a db


- [ ] more per-user permissions. (currently we only have `admin=bool`)
    - send-message
    - create-invite
    - etc


- [ ] cookie lifetimes
    - currently cookies have an infinate lifetime.
    - this should be changed by storing an end date alongside the cookie in the database
    - also should probably include this same expiration date as a max_age header so browsers will understand it automatically


- [ ] send and check verification codes sent to emails



maybe
-----
- [ ] user avatars

- [ ] invites with permissions attached to them
    - eg an invite without send-message permission


- [ ] heartbeat


- [ ] server signing cookies (cookies should be signed with (origin, useragnet, secret\_key))
    - downside is that changing IP might log you out




fixed bugs
----------
- [x] Issue #1: returned 200 for login with unrecognised username


- [x] expr\_time gets overwritten to None in create\_invite. \(only in production mode\)


- [x] fix depricated function warnings (sanitize\_uuid)


- [x] get invite crashes when using teahaz.py


implemented
-----------
- [x] replace in files: filename --> fileId; extension --> original\_name


- [x] sanitize filenames on client side
    - although on the recieving side its up to the client to call teahaz.sanitize\_filename


- [x] file transfer in chunks or sockets
    - doing chunks for now
