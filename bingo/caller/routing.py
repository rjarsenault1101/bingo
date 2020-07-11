from django.urls import path

from caller import consumers

websocket_urlpatterns = [
    path('ws/call/', consumers.CallConsumer),
    path('ws/bingo/', consumers.BingoConsumer),
    path('ws/login/', consumers.LoginConsumer),
]