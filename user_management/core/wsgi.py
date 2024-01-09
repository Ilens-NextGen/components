import os
import socketio
from django.core.wsgi import get_wsgi_application
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from streamer.views import sio
import logging
logging.basicConfig(level=logging.INFO)  

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Django WSGI application
django_app = get_wsgi_application()

# Socket.IO server
sio_app = socketio.WSGIApp(sio, django_app)

# Combine Django and Socket.IO
application = pywsgi.WSGIServer(("", 8000), sio_app, handler_class=WebSocketHandler)
# Uncomment the line below if you want to serve the application using gevent's server
application.serve_forever()
application.log = logging.get_logger()
