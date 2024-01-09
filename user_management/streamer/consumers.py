import socketio
from django.conf import settings
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=settings.CORS_ALLOWED_ORIGINS
)

socketio_app = socketio.ASGIApp(sio)

@sio.on('connect')
async def connect(sid, environ):
    print('connect ', sid)

@sio.on('disconnect')
async def disconnect(sid):
    print('disconnect ', sid)

@sio.on('clip')
async def clip(sid, timestamp, blob):
    # create a file with the timestamp as the name
    # save the blob to the file
    # send the file to the model
    # send the result back to the frontend
    
    with open(f'./{timestamp}.mp4', 'wb') as f:
        f.write(blob)
    print('clip ', timestamp)
    sio.emit('result', "Got it!")
