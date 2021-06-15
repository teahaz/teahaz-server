const chatroom = require('./teahaz.js')



const main = async(conv1) =>
{
    // create chatroom
    await conv1.create_chatroom({
        chat_name: 'conv1'
    })
    .then((res) =>
        {
            console.log(res.headers)
            console.log(conv1)
            console.log("✅ Creating chatroom successful!");
        })
    .catch((res) =>
        {
            console.log(res);
            console.error("❌ Creating chatroom failed!");
        });


    await conv1.login({
        cookie: '#'
    })
    .then((res) =>
        {
            console.log(res.headers)
            console.log(conv1)
            console.log("✅ Successfully logged in!");
        })
    .catch((res) =>
        {
            console.log(res);
            console.error("❌ Login in failed!");
        });
}




let conv1 = new chatroom({
    username: 'consumer of semen',
    password: 'slkdjflksdjfkl;sdjklfsdjlkfj',
    server: 'http://localhost:13337',
    proxy: {
        host: 'localhost',
        port: 8080
    },
    raw_response: true
});
main(conv1)






// // login
// conv1.login()
// .then((res) =>
//     {
//         // console.log(res.)
//     })
