It is not 100% sertain yet how we will have this seperate database, but it will probably be mongodb.




things to pay attention to
==========================
- In mongodb documents can only be maximum 16mb in size. For this reason any arrays inside dbs should have an uper size limit. For example cookies, classes, etc.

One way to rate liimit this is to have a maximum of 100 cookies for a user, and if they overstep this limit it deletes their oldest cookie.




Notes about examples
====================
- Every message would have its own document, thus the messages in the `messages.json` file would not be stored in a list as it is there, but rather each message would be their own document.
