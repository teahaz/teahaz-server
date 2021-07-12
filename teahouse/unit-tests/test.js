const assert = require('assert');
const chatroom = require('./teahaz.js').chatroom








const main = async(conv1) =>
{
    console.log(conv1)
}






















let conv1 = new chatroom({
      server: 'http://localhost:13337/',
      chatroomID: 'b949fa22-de46-11eb-821c-b42e99435986',
      username: 'philipsemous, consumer of semen',
      username: 'consumer of semen',
      password: 'slkdjflksdjfkl;sdjklfsdjlkfj',
      chat_name: 'conv1',
      cookie: 'bb5a5b18-de46-11eb-821c-b42e99435986',
      channels: [
        {
          channelID: 'b94e10d0-de46-11eb-821c-b42e99435986',
          channel_name: 'default',
          permissions: { r: true, w: true, x: true },
          public: true
        }
      ],
      proxy: undefined,
      raw_response: false
});
main(conv1)
