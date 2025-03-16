from django.urls import re_path
from jobchat.consumers import ChatConsumer, JobLocationConsumer, JobMatchingConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<job_id>\d+)/$', ChatConsumer.as_asgi()),  
    re_path(r'ws/jobs/(?P<job_id>\d+)/location/$', JobLocationConsumer.as_asgi()),  
    re_path(r'ws/job_matching/$', JobMatchingConsumer.as_asgi()),  # ✅ FIXED
]
