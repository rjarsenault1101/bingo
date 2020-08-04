from django.urls import path

from bingoAuth import consumers

websocket_urlpatterns = [
    path('ws/active/', consumers.ActiveConsumer),
]