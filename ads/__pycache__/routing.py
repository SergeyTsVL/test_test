# from django.urls import re_path
# from .consumers import SignalingConsumer
#
# websocket_urlpatterns = [
#     re_path(r"ws/stream/(?P<room>[\w-]+)/$", SignalingConsumer.as_asgi()),
# ]


from django.urls import re_path
from .consumers import SignalingConsumer

websocket_urlpatterns = [
    re_path(r"ws/stream/(?P<room>[^/]+)/(?P<role>streamer|viewer)/$", SignalingConsumer.as_asgi()),
]