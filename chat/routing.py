from django.urls import path
from . import consumers

# Define WebSocket URL patterns
websocket_urlpatterns = [
    path('ws/chat/<str:receiver_username>/', consumers.ChatConsumer.as_asgi()),
]

