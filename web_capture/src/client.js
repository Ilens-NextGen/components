// const baseUrl = "wss://laughing-computing-machine-gj696v7xvxw2wpw6-8000.app.github.dev/ws";
const baseUrl = "ws://localhost:8000/ws";
const client = new WebSocket(`${baseUrl}/stream/lobby/`); // this is the url of my codespace

client.onopen = () => {
    console.log("connected");
};

client.onclose = () => {
    console.log("disconnected");
};

client.onmessage = (event) => {
    console.log("response", event.data);
};
const chatClient = new WebSocket(`${baseUrl}/chat/lobby/`); // this is the url of my codespace
chatClient.onopen = () => {
    console.log("Connected to chat route");
};

chatClient.onclose = () => {
    console.log("Chat close unexpectedly");
};

export  { client, chatClient};