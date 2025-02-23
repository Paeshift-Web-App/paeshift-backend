import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "payshift.settings")
django.setup()  # Add this line

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import jobchat.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(jobchat.routing.websocket_urlpatterns)
    ),
})
