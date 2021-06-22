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
            // console.log(conv1)
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


    await conv1.send_message({
        message: "Well hello friends :^)",
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

    console.log("\n------------------------------------------------------\n")
    console.dir(conv1, { depth: null });
}




let conv1 = new chatroom({
    username: 'consumer of semen',
    password: 'slkdjflksdjfkl;sdjklfsdjlkfj',
    server: 'http://localhost:13337',
    proxy: {
        host: 'localhost',
        port: 8080
    },
    raw_response: false
});
main(conv1)






// // login
// conv1.login()
// .then((res) =>
//     {
//         // console.log(res.)
//     })
