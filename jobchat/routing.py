# chat/routing.py
from django.urls import re_path
from .consumers import ChatConsumer, JobMatchingConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<job_id>\d+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/jobs/(?P<job_id>\d+)/location/$", JobLocationConsumer.as_asgi()),

    path('ws/jobs/matching/', JobMatchingConsumer.as_asgi()),
]
