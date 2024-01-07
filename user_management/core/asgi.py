import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from image_processor.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django_asgi_app = get_asgi_application()

import image_processor.routing

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": URLRouter(websocket_urlpatterns)
    }
)