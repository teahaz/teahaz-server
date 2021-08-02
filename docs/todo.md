Security testing
================
- [ ] check wether you can supply int as arguments for username and nickname and such, and check if that is a problem





Probably but not urgent
=======================
- [ ] Remove all instances of `*.ID` to make the namespacing more consistent. (probably replace with snake_case `*._id`.




Database
========
- [x] look more into the potential switch to mongo db or some other document based database.
Currently we store a lot of data that doesnt really have relationship, would be better if it didnt have a schema and could probably be more efficiently dont with a document database. Furthermore sqlite is slow but most other databases dont support grouping like mongo db does.
On the otherhand with mongodb we would probably have to have a seperate document for every message which could get hairy I think idk.

- finish the one above





Settings
========
- [ ] Provide a setting to modify the maximum message size (text).
