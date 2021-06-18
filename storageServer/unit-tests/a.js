const chatroom = require('./teahaz.js').chatroom
const storage = require('./teahaz.js').storage






const main = async(conv1, safe) =>
{
    await conv1.create_chatroom({
        chat_name: "party"
    });

    await safe.appendItem(conv1);
    let hash = await safe.storeRemote();
    console.log('hash: ',hash , typeof(hash));
    hash = await safe.importRemote();
    console.log('hash: ',hash , typeof(hash));
    // hash = await safe.deleteRemote();
    // console.log('hash: ',hash , typeof(hash));


}


let conv1 = new chatroom({
    username: "lmfao",
    password: "whomever made party rock anthem",
    server: "http://localhost:13337/"
});

let safe = new storage({
    server: "http://localhost:13338/",
    username: "hello",
    password: "1234567890"
});

main(conv1, safe);






