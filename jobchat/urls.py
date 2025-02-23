# jobchat/urls.py
from django.urls import path
from .views import chat_room, get_messages, get_job_locations, client_list

urlpatterns = [
    path('<int:job_id>/', chat_room, name='chat_room'),
    path('api/messages/<int:job_id>/', get_messages, name='get_messages'),
    path('api/locations/<int:job_id>/', get_job_locations, name='get_job_locations'),
    path('api/clients/', client_list, name='client_list'),
]
