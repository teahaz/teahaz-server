It is not 100% sertain yet how we will have this seperate database, but it will probably be mongodb.




things to pay attention to
==========================
- In mongodb documents can only be maximum 16mb in size. For this reason any arrays inside dbs should have an uper size limit. For example cookies, classes, etc.

One way to rate liimit this is to have a maximum of 100 cookies for a user, and if they overstep this limit it deletes their oldest cookie.




Notes about examples
====================
- Every message would have its own document, thus the messages in the `messages.json` file would not be stored in a list as it is there, but rather each message would be their own document.
- Including the ID 2x in each document:
    yes, there is a real reason for this. For less processing we want to just return everything in the public object of a database when a user requests it. Which would include an ID, but mongodb wants an ID at the top of the document so we just include it 2x instead of the extra processing of inserting it manually on every request.

- There are 2 default classes. ID: 0 == constructor and ID: 1 == default
    - Everyone should be in the default class.

- The admin keyword in a class is just a shorthand for having the same rights as the constructor. (*although unlike the constructor these can still be kicked by another admin)


- Settings still have a list format, that said some settings (ie default_channel) have to be checked to be valid when they are being set


Orgnaisation of collections
===========================


```

                        maindb
                        /    \
                       /      \
                      /        \
                  multiple chatrooms
            /    |        |        |    \
           /     |        |        |     \
          /      |        |        |      \
     Users    channels classes invites   messages
       |         |       |        |          |
  Individual documents for each user, message, channel, etc
```

