const assert = require('assert');
const crypto = require('crypto');
const axios = require("axios").default;

const version = 0;
const user_agent = `teahaz.js (v ${version})`;

const print = (o) => console.dir(o, {depth: null})
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
         */
        this.users = [];

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


    async _keep_up_to_date()
    {
        /*
         * This method should be called by the constructor.
         *
         * It is supposed to make a request to the server every x
         * seconds to make sure all chatroom related variables
         * are up to date.
         */
    }

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


    /*
     *  ===========================================================================
     *   --------------------------  Exported functions  -------------------------
     *  ===========================================================================
     */

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
                "User-Agent": user_agent,
                "Content-Type": "application/json"
            },
            data: {
                "username": this.username,
                "password": this.password,
                "chatroom_name": chatroom_name || this.chatroom_name
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
                "User-Agent": user_agent,
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
            headers: {
                "User-Agent": user_agent,
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
}





module.exports = {
    chatroom: Chatroom,
}
