import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from init.models import WasActive
from django.db import connections

logger = logging.getLogger('bingo')
logger.setLevel(logging.INFO)


class ActiveConsumer(WebsocketConsumer):
    def connect(self):
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            "activity", self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            "activity", self.channel_name
        )

    # This gets called by the caller's new number button
    def receive(self, text_data):
        user = self.scope['user']
        activity = None
        try:
            activity = WasActive.objects.get(user_id=user.id)
        except WasActive.DoesNotExist:
            pass
        if activity is None:
            activity = WasActive(user_id=user.id, duration=1)
        else:
            activity.duration += 1
        activity.save()
        connections.close_all()
