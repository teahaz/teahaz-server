todos
=====
bug fixes
---------
- [ ] expr\_time gets overwritten to None in create\_invite. \(only in production mode\)

fixed bugs
----------
- [x] Issue #1: returned 200 for login with unrecognised username

upcoming
--------
- [ ] replace in files: filename --> fileId; extension --> original\_name


- [ ] file transfer in chunks or sockets


- [ ] add kid (Key ID) field to messages


- [ ] method to get a message by its id


- [ ] endpint where a user can check/change their own configs


- [ ] endpoint where the client can get some server configs that it needs to know
    - max request size
    - max stored filesize
    - does creating a chatroom require verified email


- [ ] endpoint to check chatroom configs (and some permissions should be able to change them)
    - maximum text size limit
    - not sure what else yet


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

- [ ] multiple channels in one chatroom


