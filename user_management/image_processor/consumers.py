from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .clarifai_processor import save_binary_to_file
class ImageProcessorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.type = self.scope["url_route"]["kwargs"]["type"]
        if self.type not in ["stream", "chat"]:
            print("invalid route")
            await self.close()
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"{self.type}_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        pass

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            data_type = text_data_json["type"]
            if data_type == "chat":
                message = text_data_json["message"]
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message
                    }
                )
        elif bytes_data:
            stream = bytes_data
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'stream_message',
                    'stream': stream,
                    'stream_type': 'mp4'
                }
            )

    async def chat_message(self, event):
        message = event["message"]
        # handle the logic for chatting with the ai
        # reply = ai.reply(message)
        reply = "Hi my name is Ilens and I'm pleased to be your assistant"
        await self.send(text_data=json.dumps({
            "user": message,
            "ai": reply
            }))
        
    async def stream_message(self, event):
        stream = event["stream"]
        stream_type = event["stream_type"]
        print(f"Got a {stream_type}")
        save_binary_to_file(stream, stream_type)
        await self.send(text_data=json.dumps({
            "stream": 'Successfully received stream'
            }))