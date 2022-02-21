const assert = require('assert');
const chatroom = require('./teahaz.js').chatroom

const print = (o) => console.dir(o, {depth: null});

const main = async() =>
{
    let conv1 = await new chatroom({
        server: 'http://localhost:13337',
        username: "a",
        password: "1234567890",
        nickname: "thomas",
        chatroomID: '39f1e0e8-064e-11ec-8652-b42e99435986',
        chatroom_name: "best chat",
        proxy: {host: 'localhost', port: 8080}
    }).enable();


    print(conv1);
    console.log("-----------------------------------------------------------------------------------------------");


    // creating an invite
    let invite;
    let invite_classes = ['0'];
    await conv1.create_invite({
        uses: 10,
        expiration_time: (new Date().getTime() / 1000) + 1000,
        classes: invite_classes
    })
    .then((res) =>
        {
            invite = res.data;
            console.log("✅ Created invite!");
        })
    .catch((res) =>
        {
            console.log(res);
            console.error("❌ Failed to create invite!");
            process.exit(1);
        });


    let conv2 = await new chatroom({
        server: 'http://localhost:13337',
        chatroomID: conv1.chatroomID,
        inviteID: invite.inviteID,
        username: "b",
        password: "1234567890",
        proxy: {host: 'localhost', port: 8080}
    }).enable();

    print(conv2);
}

main()
