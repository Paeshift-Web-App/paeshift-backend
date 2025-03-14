import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from jobchat.routing import websocket_urlpatterns
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "payshift.settings")
import django
django.setup()

# Import your websocket routing here
from jobchat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(  # ✅ Ensure this middleware is included
        URLRouter(websocket_urlpatterns)
    ),
})
