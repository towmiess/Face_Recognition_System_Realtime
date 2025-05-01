from django.urls import re_path
from app1.consumers import VideoStreamConsumer

websocket_urlpatterns = [
    re_path(r'^ws/video_stream/$', VideoStreamConsumer.as_asgi()),
]