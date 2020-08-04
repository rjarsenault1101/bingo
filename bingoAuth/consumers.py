import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from init.models import WasActive
import logging
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
            activity = WasActive.objects.get(
                username=user.username, team=user.email)
        except WasActive.DoesNotExist:
            pass
        if activity is None:
            activity = WasActive(username=user.username,
                                 team=user.email, duration=1)
        else:
            activity.duration += 1
        activity.save()
