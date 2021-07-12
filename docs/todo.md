Urgent fix for bazsi
====================
- [ ] Add back old method of get\_since\_time. In this case the method should exists along side the other types of get somehow, and should have some sort of rate limit of a few minutes or something similar. This function is obviously not fully thought out yet.




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




