const assert = require('assert');
const crypto = require('crypto');
const axios = require("axios").default;


// --------------------------------------- global variables ------------------------------
/*
 * USER_AGENT and version are arent
 * needed but I think its a nice to have
 * if I want to imnplement some sort of
 * warning about outdated clients later.
 */
const VERSION = 0;
const USER_AGENT = `teahaz.js (v ${VERSION})`;


// Differnt message types

/*
 * System messages are messages sent directly by the server,
 * they usually refer to some sort of envent.
 */
const SYSTEM_MESSAGE_TYPES = ['system'];


/*
 * Encoded messages (encrypted in the future) are
 * messages whose body needs to be decoded (decrpted)
 * to interpret the message.
 */
const ENCODED_MESSAGE_TYPES = ['text', 'reply-text'];

/*
 * Standard messages are messages sent by a user.
 */
const STANDARD_MESSAGE_TYPES = ['text', 'reply-text', 'file', 'reply-file'];


/*
 * Just a cool print function to save
 * some time for debugging.
 */
const print = (o) => console.dir(o, {depth: null});








// --------------------------------------- Chatroom ckass ------------------------------
/*
 *
 *  An instance of the chatroom class in teahaz.js
 *  represents all data and functions needed to interact
 *  with a single chatroom.
 *
 *  By design a user would have a list of chatroom objects,
 *  one for each chatroom they are a member of.
 *
 */
class Chatroom
{
    constructor({server, username, password, ...args})
    {
        /*
         * Server, username, and password are needed for all server functions,
         * thus these must be set.
         */
        assert(server, "Required variable 'server' has not been set.");
        assert(username, "Required variable 'username' has not been set.");
        assert(password, "Required variable 'password' has not been set.");
        this.server = server;
        this.username = username;
        this.password = password;

        /*
         * Nickname is optional, if it is not set
         * then the server will set it to the same as username
         */
        this.nickname = args.nickname;

        /*
         * Although chatroomID is crusial for the server running,
         * it is not needed for create chatroom, as there the server
         * assings a new chatroomID.
         *
         * It is however needed for every other function.
         */
        this.chatroomID = args.chatroomID;

        /*
         * The proxy variable is mostly for debugging,
         * with this you can set the client to run through
         * burp or zap.
         *
         * format = {
         *      host: 'url',
         *      port: int
         * }
         */
        this.proxy = args.proxy;

        /*
         * A single string storing the cookie value.
         *
         * This needs to be paired up with the chatroomID
         * to make a valid cookie.
         */
        this.cookie = '';

        /*
         * The channels variable holds an array of all channels on the chatroom.
         *
         * (for one channel)
         * format = [
         *      {
         *        channelID: '9541e2de-ecc9-11eb-b7fd-b42e99435986',
         *        name: 'default',
         *        permissions: [
         *            {
         *               classID: '1',
         *               r: true,
         *               w: true,
         *               x: false
         *            }
         *         ]
         *      }
         * ]
         */
        this.channels = [];

        /*
         * The classes variable holds an array of all user classes
         * on the chatroom.
         *
         * format = [
         *      { classID: '0', name: 'constructor' },
         *      { classID: '1', name: 'default' }
         *    ],
         */
        this.classes = [];

        /*
         * The users variable stores an array of all the members of
         * the chatroom. It also stores some important information about
         * each user.
         *
         * format = [
         *    {
         *      classes: [ '0', '1' ],
         *      colour: { b: null, g: null, r: null },
         *      nickname: 'consumer of semen',
         *      username: 'consumer of semen'
         *    }
         * ]
         *
         * Add what information we have about our user to this array.
         * All of this will likely be overwritten anyway, but might help.
         */
        this.users = [{
            username,
            nickname: args.nickname,
            colour: args.colour
        }];

        /*
         * The settings variable contains an array of all of the server settings.
         *
         * Why is this in an array and not an object/mapping?
         * There are a few reasons for this:
         *  1. Having arrays allows us to store the name, value and type together easily.
         *  2. Due to the way the server works, its much easier for the server
         *      to return them like this.
         *  3. While we could convert them to an object locally, it would mean that it
         *      needs to be updated every time there is a minor setting added to the server.
         *
         * format = [
         *      { sname: 'chatroom_name', stype: 'string', svalue: 'conv1' },
         *      { sname: 'min_password_length', stype: 'int', svalue: 10 },
         *      {
         *        sname: 'default_channel',
         *        stype: 'string',
         *        svalue: 'e796d4d6-ed46-11eb-b3b2-b42e99435986'
         *      }
         *  ]
         *
         */
        this.settings = [];


        /*
         * Set everything that wasnt explicitly set.
         *
         * Anything that falls in this probably should not be set,
         * but there is no reason to restrict it I guess.
         */
        for (const key in args)
            this[key] = args[key];
    }

    /*
     * Proper encryption is not yet inplemented in teahaz,
     * so for now we are just using base64 encoding.
     *
     * This will obviously not stay like this.
     */
    _encode(text) { return Buffer.from(text, 'binary').toString('base64'); } // placeholder for encryption
    _decode(text) { return Buffer.from(text, 'base64').toString('binary'); } // placeholder for decryption


    _runcallbacks(callback, arg)
    {
        /*
         * This is a small helper function to deal with callbacks.
         *
         * It is needed because callbacks are optional arguments,
         * and I dont want to test if they are defined every time I 
         * use one. (They are called a lot)
         */
        if (callback != undefined)
        {
            callback(arg)
        }
    }

    _extract_cookie(server_response)
    {
        /*
         * Cookies from the server are set via the set-cookie
         * header. However axios doesnt have a good way to 
         * handle them so I have this function which needs to
         * get called after each request to save the cookies.
         *
         */
        let temp = [];

        // cookies are sent back from the server via the `set-cookie` header
        temp = server_response.headers['set-cookie']

        // make sure that there was actually a cookie set
        if (temp && temp != undefined)
            temp = temp[0].split('; ')[0].split('=');
        else
            return

        // loop through the cookies and find the one for this chatroom
        for(let i=0; i<temp.length; i++)
        {
            if (temp[i] == this.chatroomID)
            {
                // save cookie
                this.cookie = temp[i+1]
            }
        }
    }

    _store_default_join(response)
    {
        this.chatroom_name = response.data.chatroom_name;
        this.chatroomID    = response.data.chatroomID;
        this.settings      = response.data.settings;
        this.channels      = response.data.channels;
        this.classes       = response.data.classes;
        this.users         = response.data.users;

        // save cookie
        this._extract_cookie(response);
    }

    _get_user_info(username)
    {
        /*
         * Get all locally stored information
         * about a user.
         *
         * This would really be used to get a nickname
         * or a colour.
         */
        for (const user of this.users)
        {
            if (username == user.username)
                return user
        }
    }

    _add_user_info_message(message)
    {
        // system messages are good as they are
        if (SYSTEM_MESSAGE_TYPES.includes(message.type))
            return message


        /*
         * Try find the user that sent
         * the message in the users list.
         *
         * If it could find it then set
         * the nickname variable.
         */
        for (const u of this.users)
            if (message.username == u.username)
                message.nickname = u.nickname;


        /*
         * If there is no user with that name,
         * then use their username instead.
         *
         * Im not entirely sure about this move
         * as im not sure we should be displaying
         * the users username.
         * This is not a security reason, just that
         * the username is unchangable and it might
         * make it worse for some users.
         */
        if (message.nickname == undefined)
            message.nickname = message.username;


        // Encoded messages have to be decoded
        if (ENCODED_MESSAGE_TYPES.includes(message.type))
            message.text = this._decode(message.data)

        return message
    }

    /*
     *  ===========================================================================
     *   --------------------------  Exported functions  -------------------------
     *  ===========================================================================
     */


    // ==================================== Local / modifier functions ============================================
    async enable({type, ...args}={})
    {
        /*
         * The enable function is a shorthand for
         * create, login or use invite to join a chatroom.
         *
         * The main purpose of this function is so that you
         * can do something like: "c = new chatroom({data}).enable()",
         * without having to explicitly do this afterwards
         *
         * types:
         *  - 0 == create chatroom
         *  - 1 == login to chatroom
         *  - 2 == use invite
         *  - undefined == It is inferred from the supplied variables
         *
         *
         *  How the function guesses what you want to do:
         *      if chatroomID is not set: create_chat
         *      if inviteID is set: use invite
         *      else: login
         */

        if (type == undefined)
        {
            if (!this.chatroomID)
                type = 0;

            else if (args.inviteID || this.inviteID)
                type = 2;

            else
                type = 1
        }

        let res;
        switch (type)
        {
            case 0:
                return await this.create(args)
                .then((_) =>
                    {
                        return Promise.resolve(this)
                    })
                .catch((res) =>
                    {
                        return Promise.reject(res)
                    })

            case 1:
                return await this.login(args)
                .then((_) =>
                    {
                        return Promise.resolve(this)
                    })
                .catch((res) =>
                    {
                        return Promise.reject(res)
                    })

            case 2:
                // return await this.use_invite(args)
                // .then((_) =>
                //     {
                //         return Promise.resolve(res)
                //     })
                // .catch((res) =>
                //     {
                //         return Promise.reject(res)
                //     })
                res = 'use_invite not implemented yet';
                return res;
        }
    }


    // ==================================== server functions ======================================================


    async create({chatroom_name, callback_success, callback_error}={})
    {
        /*
         * Method creates a new chatroom with the specified 'chatroom_name'.
         *
         * This method is also one of the 3 ways of getting a cookie
         * for a chatroom.
         */

        // Make sure the chatroom name has been set
        assert((chatroom_name || this.chatroom_name), "'chatroom_name' (name of the chatroom) has not been set!");

        return axios({
            method: 'post',
            url: `${this.server}/api/v0/chatroom/`,
            header: {
                "User-Agent": USER_AGENT,
                "Content-Type": "application/json"
            },
            data: {
                "username": this.username,
                "password": this.password,
                "chatroom-name": chatroom_name || this.chatroom_name
            },
            proxy: this.proxy
        })
        .then((response) =>
            {
                // save chatroom details
                this._store_default_join(response)

                this._runcallbacks(callback_success, response);
                return Promise.resolve(response);
            })
        .catch((response) =>
            {
                this._runcallbacks(callback_error, response);
                return Promise.reject(response);
            })
    }

    async login({callback_success, callback_error}={})
    {
        /*
         * Method attempts to login to a chatroom.
         *
         * This method is also one of the 3 ways of getting a cookie
         * for a chatroom.
         */
        assert(this.username , "'username' variable has not been set.");
        assert(this.password , "'password' variable has not been set.");
        assert(this.chatroomID , "'chatroomID' variable has not been set.");


        return axios({
            method: 'post',
            url: `${this.server}/api/v0/login/${this.chatroomID}`,
            header: {
                "User-Agent": USER_AGENT,
                "Content-Type": "application/json"
            },
            data: {
                "username":   this.username,
                "password":   this.password,
            },
            proxy: this.proxy
        })
        .then((response) =>
            {
                // save chatroom details
                this._store_default_join(response)

                this._runcallbacks(callback_success, response);
                return Promise.resolve(response);
            })
        .catch((response) =>
            {
                this._runcallbacks(callback_error, response);
                return Promise.reject(response);
            })
    }

    async get_chat_info({callback_success, callback_error}={})
    {
        /*
         * Method attempts to get standard join information
         * about a chatroom.
         *
         * This method can also be used to check if the client
         * is logged in / has a valid cookie.
         */

        assert(this.username , "'username' variable has not been set.");
        assert(this.chatroomID , "'chatroomID' variable has not been set.");


        return axios({
            method: 'get',
            url: `${this.server}/api/v0/chatroom/${this.chatroomID}`,
            headers:
            {
                "User-Agent": USER_AGENT,
                "Content-Type": "application/json",
                "Cookie": `${this.chatroomID}=${this.cookie}`,
                username: this.username
            },
            proxy: this.proxy
        })
        .then((response) =>
            {
                // save chatroom details
                this._store_default_join(response)

                this._runcallbacks(callback_success, response);
                return Promise.resolve(response);
            })
        .catch((response) =>
            {
                this._runcallbacks(callback_error, response);
                return Promise.reject(response);
            })
    }

    async create_channel({channel_name, permissions, callback_success, callback_error}={})
    {
        /*
         * Create a new channel in the chatroom.
         *
         * This currently can only be done by a chatroom admin.
         */

        assert(this.username, "'chatroomID' variable is undefined.");
        assert(this.chatroomID, "'chatroomID' variable is undefined.");
        assert(channel_name, "'channel_name' variable has not been set.");

        // if no permissions are set then just have some sane defaults
        if (permissions == undefined)
            permissions = [
                {
                    classID: '1',
                    r: true,
                    w: true,
                    x: false
                }
            ];

        return axios({
            method: 'post',
            url: `${this.server}/api/v0/channels/${this.chatroomID}`,
            headers:
            {
                "User-Agent": USER_AGENT,
                "Content-Type": "application/json",
                "Cookie": `${this.chatroomID}=${this.cookie}`
            },
            data:
            {
                "username": this.username,
                "channel-name": channel_name,
                "permissions": permissions
            }
        })
        .then((response) =>
            {
                this.channels.push(response.data);

                this._runcallbacks(callback_success, response);
                return Promise.resolve(response);
            })
        .catch((response) => 
            {
                this._runcallbacks(callback_error, response);
                return Promise.reject(response);
            });
    }

    async send_message({message, channelID, replyID, callback_success, callback_error}={})
    {
        assert(typeof(message) == 'string', "'message' has to be of type string.")
        assert(channelID, "'channelID' variable has not been set!")

        // keep unencoded message for the return
        // (there is no need to decode it)
        let message_text = message;

        // We need to encode messages to simulate the encryption we will have later.
        message = this._encode(message);

        return axios({
            method: 'post',
            url: `${this.server}/api/v0/messages/${this.chatroomID}`,
            headers:
            {
                "User-Agent": USER_AGENT,
                "Content-Type": "application/json",
                "Cookie": `${this.chatroomID}=${this.cookie}`
            },
            data:
            {
                username: this.username,
                data: message,
                channelID,
                replyID
            }
        })
        .then((response) =>
            {

                // Add some info like nickname and decoded message to the message.
                response.data = this._add_user_info_message(response.data);

                this._runcallbacks(callback_success, response);
                return Promise.resolve(response);
            })
        .catch((response) => 
            {
                this._runcallbacks(callback_error, response);
                return Promise.reject(response);
            });
    }

    async get({time, channelID, callback_success, callback_error}={})
    {
        assert(typeof(time) == 'number', "'time' variable has to be a number.");

        // Due to the limitations of the http standard
        // we have to send information for GET requests
        // in the header.
        let headers = {
            "User-Agent": USER_AGENT,
            "Content-Type": "application/json",
            "Cookie": `${this.chatroomID}=${this.cookie}`,

            "username": this.username,
            "time": time,
        }

        // Axios doesnt allow you to send undefined in a header
        // so the channelID will only be set if its defined.
        //
        if (typeof(channelID) != "undefined")
            headers['channelID'] = channelID

        return axios({
            method: 'get',
            url: `${this.server}/api/v0/messages/${this.chatroomID}`,
            headers: headers
        })
        .then((response) =>
            {
                // Add some info like nickname and decoded message to the message.
                let messages_array = []
                for (const m of response.data)
                {
                    messages_array.push(this._add_user_info_message(m));
                }
                response.data = messages_array;

                this._runcallbacks(callback_success, response);
                return Promise.resolve(response);
            })
        .catch((response) => 
            {
                this._runcallbacks(callback_error, response);
                return Promise.reject(response);
            });
    }
}





module.exports = {
    chatroom: Chatroom,
}
