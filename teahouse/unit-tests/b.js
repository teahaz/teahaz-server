const util = require('util')
const assert = require('assert');
const chatroom = require('./nth.js').chatroom


const print = (o) => console.dir(o, {depth: null})


conv = new chatroom({
    server: 'http://localhost:13337',
    username: "a",
    password: "1234567890",
    nickname: "thomas"
});

conv.create({
    chat_name: "best chatroom"
})
.then(() =>
    {
        print(conv);
    })


