import socketio
from django.conf import settings
import asyncio
from random import choice
from image_processor.clarifai_processor import (
    AsyncVideoProcessor, AsyncClarifaiImageRecognition
    )

MOCK_AI_RESPONSES = [
    "Hello! How can I assist you today?",
    "I'm here to help. What do you need?",
    "Greetings! What can I do for you?",
    "Good day! Ask me anything.",
    "Hi there! Ready for a chat?",
    "Welcome! How may I be of service?",
    "Hey! What brings you here?",
    "Greetings! Feel free to ask me questions.",
    "Hello! I'm at your disposal. What's on your mind?",
    "Hi! Let's chat about anything you like.",
]
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=settings.CORS_ALLOWED_ORIGINS
)


# @sio.on('connect')
# async def connect(sid, environ):
#     print('connect ', sid)

# @sio.on('disconnect')
# async def disconnect(sid):
#     print('disconnect ', sid)

# @sio.on('clip')
# async def clip(sid, timestamp, blob):
#     # create a file with the timestamp as the name
#     # save the blob to the file
#     # send the file to the model
#     # send the result back to the frontend
    
#     with open(f'./{timestamp}.mp4', 'wb') as f:
#         f.write(blob)
#     print('clip ', timestamp)
#     sio.emit('result', "Got it!")
class ChatNamespace(socketio.AsyncNamespace):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_image = []
    async def on_connect(self, sid, environ):
        room_id = sid
        print("Roomid", room_id)
        # user = authenticate(room_id) # Authenticate the user later
        #if not user:
        #   await self.disconnect("no user found")
        self.room_id = room_id
        self.video_processor = AsyncVideoProcessor()
        self.find_obstacles = AsyncClarifaiImageRecognition()
        await sio.enter_room(sid, room_id)
        print('Connected', sid)


    def get_room_id(self, environ):
        namespace = environ.get('PATH_INFO', '/').split('/')[2]
        room_id = namespace.split('/')[-1]
        print(room_id)
        return room_id


    async def on_disconnect(self, sid):
        print('Disconnected', sid)
        await sio.leave_room(sid, self.room_id)

    async def on_clip(self, sid, timestamp, blob: bytes):
        image_list = await self.video_processor.process_video(blob)
        image_bytes_list = self.video_processor.convert_result_image_arrays_to_bytes(image_list)
        print('clip ', timestamp)
        await sio.emit('finished_frame', image_bytes_list[-1], room= self.room_id)
        print("Done converting")
        await asyncio.to_thread(self.find_obstacles.find_all_objects, [image_bytes_list[-1]])
        await sio.emit('result', "There's a car in front of you. Watch out", room=self.room_id)

    async def on_question(self, sid, question):
        async def on_finished_frame(self, sid, image_bytes_list):
            print("Frame received")
        await sio.emit('ai_reply', choice(MOCK_AI_RESPONSES), room= self.room_id)
    
sio.register_namespace(ChatNamespace('/'))
socketio_app = socketio.ASGIApp(sio)
