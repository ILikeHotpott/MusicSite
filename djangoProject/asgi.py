"""
ASGI config for djangoProject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from djangoProject import routing


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject.settings")

# application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # 自动找urls.py, views.py --> http
    "websocket": URLRouter(routing.websocket_urlpatterns),  # routings(urls), consumers(views)
})
