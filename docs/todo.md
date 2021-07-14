Security testing
================
- [ ] check wether you can supply int as arguments for username and nickname and such, and check if that is a problem





Unify chatroom information
==========================
login/register returns

channels
--------
(channels are an un-unified mess)
- [ ] Some sort of unification between get\_readable\_channels and fetch\_all channels.
- [ ] Sorting out a bunch of other channels mess.
- [ ] Replace `public` property of channels with `rw` and have that apply by default with all classes overriding it.
- [ ] Maybe dont replace above for speed idk


Speed increase and clarity
==========================
- [ ] Try use slightly smarter sql to check if a user can read from chatroom in one sql query.


Probably but not urgent
=======================
- [ ] Remove all instances of `*.ID` to make the namespacing more consistent. (probably replace with snake_case `*._id`.




Database
========
- [ ] look more into the potential switch to mongo db or some other document based database.
Currently we store a lot of data that doesnt really have relationship, would be better if it didnt have a schema and could probably be more efficiently dont with a document database. Furthermore sqlite is slow but most other databases dont support grouping like mongo db does.
On the otherhand with mongodb we would probably have to have a seperate document for every message which could get hairy I think idk.
