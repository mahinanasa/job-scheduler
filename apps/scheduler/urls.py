from django.urls import re_path
from .consumers import JobConsumer  # Replace with your WebSocket consumer

websocket_urlpatterns = [
    re_path(r"ws/jobs/$", JobConsumer.as_asgi()),  # Match the frontend WebSocket URL
]
