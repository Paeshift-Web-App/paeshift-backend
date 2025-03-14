import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from jobchat.routing import websocket_urlpatterns

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "payshift.settings")

# Setup Django
django.setup()

# Define ASGI application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
