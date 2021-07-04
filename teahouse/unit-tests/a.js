const util = require('util')
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
        });




    await conv1.login()
    .then((res) =>
        {
            // console.log(res.headers)
            // console.log(res)
            console.log("✅ Successfully logged in!");
        })
    .catch((res) =>
        {
            console.log(res);
            console.error("❌ Login in failed!");
        });


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
        });


    // let i = 0;
    // while (i < 1000)
    // {
        await conv1.send_message({
            message: `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA`,
            channelID: conv1.channels[0].channelID
        })
        .then((res) =>
            {
                // console.log(conv1)
                // console.log(res)
                console.log("✅ Message sent!");
            })
        .catch((res) =>
            {
                console.log(res);
                console.error("❌ Failed to send message!");
            });
        // i += 1
    // }



    //
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
        });
    //
    //

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
        });



    await conv1.get_messages({
        count: 5,
        // start_time: 1624611669.907108,
        channelID: conv1.channels[0].channelID
    })
    .then((res) =>
        {
            // console.log(res)
            console.log("✅ Got messages");
        })
    .catch((res) =>
        {
            console.log(res);
            console.error("❌ Failed to get messages!");
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
        });

    await conv1.create_invite({
        uses: 10,
        bestbefore: 1625462441.6239355
    })
    .then((res) =>
        {
            conv1.invite = res.inviteID;
            console.log("✅ Created invite!");
        })
    .catch((res) =>
        {
            console.log(res);
            console.error("❌ Failed to create invite!");
        });


    await conv1.use_invite({
        inviteID: conv1.invite,
        username: 'hehehehehe',
        password: 'newpw, very cool!'
    })
    .then((res) =>
        {
            console.log(res)
            console.log("✅ Used invite to join chatroom");
        })
    .catch((res) =>
        {
            console.log(res);
            console.error("❌ Failed to use invite");
        });

    console.log(conv1)

    console.log("\n------------------------------------------------------\n")
    // console.dir(conv1, { depth: null });
}




let conv1 = new chatroom({
    username: 'consumer of semen',
    password: 'slkdjflksdjfkl;sdjklfsdjlkfj',
    server: 'http://localhost:13337/',


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
