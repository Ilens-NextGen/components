import io from "socket.io-client";
import $ from "jquery";


const client = io("https://laughing-computing-machine-gj696v7xvxw2wpw6-8000.app.github.dev", {
    transports: ["websocket", "polling", "flashsocket"],
});

client.on("connect", () => {
    console.log("connected");
})

client.on("disconnect", () => {
    console.log("disconnected");
})

client.on("response", (data) => {
    console.log("response", data);
})
client.on('ai_reply', (data) => {
    let result = data;
    console.log("result", result);
    $("#chat-log").append(`<li class='ai'>${result}</li>`);
});
export default client;
