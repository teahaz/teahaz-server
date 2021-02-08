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


register
--------
[ ] /register will happily register multiple users with the same username and or email


code review
===========
this is not really a todo but a list of things i have already done

[done] /login
[done] /register

[in progress] /message

[ ] /file
[ ] everything else


bug fixes
=========

[ ] crash when json is not sent on login (probably in other places as well), this should just error

[ ] `save_in_db` and `get_messages` doesnt encode as it should

