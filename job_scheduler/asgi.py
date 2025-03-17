import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apps.scheduler.urls import websocket_urlpatterns  # Import WebSocket routes

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "job_scheduler.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # For HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # For WSS requests
        )
    ),
})
