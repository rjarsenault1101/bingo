import json, random
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async

from init.models import Callable
from .models import CalledNumber

class CallConsumer(WebsocketConsumer):
    def connect(self):
        # Send all the current values? 
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            "numbercalling", self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            "numbercalling", self.channel_name
        )

    # This gets called by the caller's new number button
    def receive(self, text_data):
        callable_items = Callable.objects.values('value').exclude(value__in=CalledNumber.objects.all().values_list('number', flat=True)).values_list('value', flat=True)
        callable_items = list(callable_items)
        new_number = CalledNumber(number=int(random.choice(callable_items)))
        new_number.save()
        async_to_sync(self.channel_layer.group_send)(
            "numbercalling",
            {
                'type': 'caller_number',
                'number': new_number.number
            }
        )

    # Push new number to everyone
    def caller_number(self, event):
        newNumber = event['number']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'number': newNumber
        }))