Error checking
==============
- [ ] Make sure there is a check for None (not found) after every fetch from the database.


Settings
========
- [ ] Provide a setting to modify the maximum message size (text).


Permissions
===========
- [ ] Add more granular permission settings in class objects.
Currently the only information other than id and name stored in a class obj is `admin=bool`. I should change this to a more granular permission system where it can hold many different settings. (eg: `can_create_invite=bool` or `manage_messages=bool`)


Fix naming inconsistencies (maybe)
==================================
- [ ] Remove all instances of `*.ID` to make the namespacing more consistent. (probably replace with snake_case `*._id`.

