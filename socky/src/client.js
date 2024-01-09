import io from "socket.io-client";

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

export default client;
