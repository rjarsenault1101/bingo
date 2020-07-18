from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from caller.consumers import BingoConsumer, CallConsumer
from django.conf.urls import url

application = ProtocolTypeRouter({
     "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^ws/bingo/$", BingoConsumer),
            url(r"^ws/call/$", CallConsumer),
        ])
    ),
})