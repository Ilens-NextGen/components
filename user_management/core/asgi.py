import os
import socketio
from django.core.asgi import get_asgi_application
from streamer.views import sio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django_asgi_app = get_asgi_application()

application = socketio.ASGIApp(sio, django_asgi_app)
from django.core.wsgi import get_wsgi_application
from socketio_app.views import sio

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_socketio.settings');

django_app  = get_wsgi_application();
application = socketio.WSGIApp(sio, django_app);

####################################################################################

from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

server = pywsgi.WSGIServer(("", 8000), application, handler_class=WebSocketHandler);
server.serve_forever();
