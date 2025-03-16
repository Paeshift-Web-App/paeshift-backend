import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# ✅ Set environment variable for Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "payshift.settings")

# ✅ Ensure Django apps are loaded before importing anything else
django.setup()

# ✅ Now import WebSocket routes AFTER `django.setup()`
from jobchat.routing import websocket_urlpatterns

# ✅ Define the ASGI application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handles HTTP requests
    "websocket": AuthMiddlewareStack(  # Handles WebSocket connections
        URLRouter(websocket_urlpatterns)
    ),
})
