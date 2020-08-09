# bazsi 


### things i should implement:
	- command support:
		X !clr for os.system('clear')
		X !st for showTime
		X !si for showIcon
		!res to restore all messages

	- color system:
		colors.py file has all the colors
		
		self = <hex/rgb value>
		partner = <hex/rgb value>

		the program default to b/w, unless it finds colors set
	
	- restore old messages + toggle showing messages not from current session

	- clean up input.py

	- possibly look into threading the input and not the listenero


### things the other person should implement:
	- maybe we could have a way to message different people specifically and have separate connection
        my idea is that we can have a hub on like port 8000 and for each connection it will throw you on a pre defined port
        kinda like channels, would also mean that you can skip the "hub" by just connecting on the port your dm/group is on
            honestly we might not even need the "hub" just a text file that says "dm with bazsi = port 8001 /n group with sleep parlysis demons = 8006"

        obvious issue: this wont scale well but for now it might be good? [im pretty sure my server could only handle listning on like 50 ports max]
            [ i mean if you think about it its self hosted so at any one server there will only be so many connections]

    

### bugs
	- clr only refreshes once someone has sent a message after it and calling client.send directly seems to cause a hang
	- not really a bug but i should remove the logger thing since it doesnt do much

### fixed
	- changing data to message broke display

### recently done
	- make the screen clear on exit if it's even possible
    - added autologin file
	- rudimentary command handler system
		input creates a file with the command inside, display handles it and deletes the file

    
    







# me


### things i should implement:
    - authentication of clint
        this is being done in the authenticaton branch


### things the other person should implement:
    

### bugs
    - method GET has troubles handling large amounts of data    
        should not be a problem under 100 lines, but needs to be fixed regardless

### fixed


### recently done
    - fixed inconsistancy in incoming messages
        its all "mesage" now
    - added sender time to messages 
        epoch time format[ time.time() ]
    - finished the base of authenticaton


### actual notes
    - username and password will be hashed before sending
        not bc it would add more security but i wouldnt need to sanitize them, and base64 seems like a bad idea for some reason
    - when sending username and password, they will be seperated by whitespace
        this is okay bc they will be hashed without allowing for whitespace


#fyi
### server
i need to add a small tutorial for adding auth, idk if this is good enough but hey its best i can do
    - to start with i already did it in a file called `client/input_with_auth_example_but_i_broke_it.py` 
    on the other the order of conneting to the server is
        - connect
        - socket test [thing that was formerly a tmp fix for a timing issue, (instead of fixing i made it into something useful)]
        - authenticate(session, password_auth=True, username="", password="", path_to_saved_creds="./.creds")
            so there are lots of args for this so i need to explain them
            1: you always need to add the session
            2: password_auth=True/false: when  you first connect there are no saved creds so you should supply a username and a password
                fyi: this is not registering, {thats not implemented yet lmao}
                when the device has logged in before it saves the creds (the password is encrypted) for autologin, 
                if you want autologin just say password_auth=False and dont give a username and password
                
            3: username should be obvi, again this is only if password auth is true
            4: password should be obvi, again this is only if password auth is true

            5: this is the path to the saved creds/where they should be saved. (its in json format so dont shout at me)
                if you have password_auth=false it will use creds here to log in
                else it will save creds here
                the username is unencrypted so you can use it instead of `name` in the code

    ### i need to add 2 things to the text above, 
            1: if i said anywhere that autologin doesnt work, then its a lie bc i fixed it (my comments are more bloated then the code lmao)
            2: check out client/testers/authTest.py for a commented example of how to use it

i feel like i need to add an explentaion for my abuse of the json format
    i store data line by line bc this way i can read and process a line without putting the whole file into memory
    this is normal tho i dont know any implementation that uses json with this
    but really why not, python is slow enough this wont make much of a difference, this is a messaging app not a game, that extra ~3ms wont matter
