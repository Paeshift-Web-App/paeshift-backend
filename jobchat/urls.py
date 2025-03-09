# jobchat/urls.py
from django.urls import path
from .views import *
urlpatterns = [
    path('chat/<int:job_id>/', chat_room, name='chat_room'),
    path('api/messages/<int:job_id>/', get_messages, name='get_messages'),
    path('api/locations/<int:job_id>/', get_job_locations, name='get_job_locations'),
]


# http://localhost:8000/chat/room/2/
