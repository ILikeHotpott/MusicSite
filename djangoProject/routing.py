from django.urls import re_path
from app01 import consumers

websocket_urlpatterns = [
    # ws://127.0.0.1:8000/room/qq_group_num/
    re_path(r'ws/chat/(?P<sender>\w+)_(?P<receiver>\w+)/$', consumers.ChatConsumer.as_asgi()),
]