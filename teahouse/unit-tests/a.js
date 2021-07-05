const util = require('util')
const assert = require('assert');
const chatroom = require('./teahaz.js').chatroom



const main = async(conv1) =>
{
    // create chatroom
    await conv1.create_chatroom({
        chat_name: 'conv1'
    })
    .then((res) =>
        {
            // console.log(res.headers)
            console.dir(conv1, {depth: null})
            console.log("\n------------------------------------------------------\n")
            console.log("✅ Creating chatroom successful!");
        })
    .catch((res) =>
        {
            console.log(res);
            console.error("❌ Creating chatroom failed!");
            process.exit(1);
        });


    //
    //
    // await conv1.login()
    // .then((res) =>
    //     {
    //         // console.log(res.headers)
    //         // console.log(res)
    //         console.log("✅ Successfully logged in!");
    //     })
    // .catch((res) =>
    //     {
    //         console.log(res);
            // console.error("❌ Login in failed!");
            // process.exit(1);
    //     });


    await conv1.check_login()
    .then((res) =>
        {
            // console.log(res.headers)
            // console.log(conv1)
            console.log("✅ Checked login!");
        })
    .catch((res) =>
        {
            console.log(res);
            console.error("❌ Checking login failed!");
            process.exit(1);
        });


    await conv1.create_channel({
        channel_name: "memes channel",
        public_channel: true
    })
    .then((res) =>
        {
            // console.log(res)
            console.log("✅ Created new channel");
        })
    .catch((res) =>
        {
            console.log(res);
            console.error("❌ Failed to create channel!");
            process.exit(1);
        });

    await conv1.get_channels()
    .then((res) =>
        {
            // console.log(res)
            // console.log(conv1)
            console.log("✅ Got channels!");
        })
    .catch((res) =>
        {
            console.log(res, { depth: null });
            console.error("❌ Failed to get channels!");
            process.exit(1);
        });


    let middle_message_time = 0;
    let i = 0;
    while (i < 100)
    {
        // send 100 messages to differnt channels
        await conv1.send_message({
            message: `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA`,
            channelID: conv1.channels[i%2].channelID
        })
        .then((res) =>
            {
                // console.log(conv1)
                // console.log(res)
            })
        .catch((res) =>
            {
                console.log(res);
                console.error("❌ Failed to send message!");
            });

        if (i == 49)
            middle_message_time = new Date().getTime() / 1000

        // await conv1._sleep(500)
        i += 1
    }
    console.log("✅ sent 100 messages!");







    await conv1.monitor_messages({
        since: 0
    })
    .then((res) =>
        {
            console.log(res);
            // console.log('got:', res.length);


            let seen = []
            for (const message of res)
            {
                assert(!seen.includes(message.messageID), "wtf");
                seen.push(message.messageID);
            }
            // assert(res.length == 50, "Got wrong amount of messages");
            console.log("✅ Got messages since <time>");
            // process.exit(1);
        })
    .catch((res) =>
        {
            console.log(res);
            console.error("❌ Failed to get messages!");
            process.exit(1);
        });


    await conv1.get_messages({
        count: 100,
        // start_time: 1624611669.907108,
        // channelID: conv1.channels[0].channelID
    })
    .then((res) =>
        {
            // console.log(res.length);
            // assert(res.length == 5, "Got wrong amount of messages!");
            console.log("✅ Got <count> messages!");
        })
    .catch((res) =>
        {
            console.log(res);
            console.error("❌ Failed to get messages!");
            process.exit(1);
        });


    await conv1.get_messages({
        count: 100,
        start_time: middle_message_time,
        // channelID: conv1.channels[0].channelID
    })
    .then((res) =>
        {
            // console.log(res.length);
            assert(res.length == 51, "Got wrong amount of messages!");
            console.log("✅ Got <count> messages with start_time!");
        })
    .catch((res) =>
        {
            console.log(res);
            console.error("❌ Failed to get messages!");
            process.exit(1);
        });




    await conv1.monitor_messages({
        count: 5,
        since: middle_message_time,
        channelID: conv1.channels[0].channelID
    })
    .then((res) =>
        {
            // console.log(res.length)

            // check if everything worked
            for (const msg of res)
                assert(msg.channelID == conv1.channels[0].channelID, "Failed to filter ot one channel!")

            console.log("✅ Got messages since <time> with channel filter.");
        })
    .catch((res) =>
        {
            console.log(res);
            console.error("❌ Failed to get messages!");
            process.exit(1);
        });


    await conv1.get_messages({
        count: 5,
        // start_time: 1624611669.907108,
        channelID: conv1.channels[1].channelID
    })
    .then((res) =>
        {
            // console.log(res.length);

            // check if everything worked
            for (const msg of res)
                assert(msg.channelID == conv1.channels[1].channelID, "Failed to filter ot one channel!")

            // assert(res.length == 5, "Got wrong amount of messages!");
            console.log("✅ Got <count> messages with channel filter.");
        })
    .catch((res) =>
        {
            console.log(res);
            console.error("❌ Failed to get messages!");
            process.exit(1);
        });


    await conv1.get_messages({
        count: 100,
        start_time: middle_message_time,
        channelID: conv1.channels[0].channelID
    })
    .then((res) =>
        {
            // console.log(res.length);

            // check if everything worked
            for (const msg of res)
                assert(msg.channelID == conv1.channels[0].channelID, "Failed to filter ot one channel!")

            // assert(res.length == 51, "Got wrong amount of messages!");
            console.log("✅ Got <count> messages with start_time and channel filter");
        })
    .catch((res) =>
        {
            console.log(res);
            console.error("❌ Failed to get messages!");
            process.exit(1);
        });








    await conv1.get_users()
    .then((res) =>
        {
            // console.log(res)
            console.log("✅ Got users");
        })
    .catch((res) =>
        {
            console.log(res);
            console.error("❌ Failed to get users!");
            process.exit(1);
        });

    await conv1.create_invite({
        uses: 10,
        expiration_time: (new Date().getTime() / 1000) + 1000
    })
    .then((res) =>
        {
            conv1.invite = res.inviteID;
            // console.log(res)
            console.log("✅ Created invite!");
        })
    .catch((res) =>
        {
            console.log(res);
            console.error("❌ Failed to create invite!");
            process.exit(1);
        });


    await conv1.use_invite({
        inviteID: conv1.invite,
        username: 'hehehehehe',
        password: 'newpw, very cool!'
    })
    .then((res) =>
        {
            // console.log(res)
            console.log("✅ Used invite to join chatroom");
        })
    .catch((res) =>
        {
            console.log(res);
            console.error("❌ Failed to use invite");
        });


    console.log("\n------------------------------------------------------\n")
    console.dir(conv1, { depth: null });
}




let conv1 = new chatroom({
    username: 'consumer of semen',
    password: 'slkdjflksdjfkl;sdjklfsdjlkfj',
    server: 'http://localhost:13337/',
    // server: 'https://teahaz.co.uk',


    // // use the same chatroom
    // chatroomID: '9a9acf74-d591-11eb-b454-b42e99435986',
    // userID: '0',
    //
    // proxy: {
    //     host: 'localhost',
    //     port: 8080
    // },
    raw_response: false
});
main(conv1)






// // login
// conv1.login()
// .then((res) =>
//     {
//         // console.log(res.)
//     })
