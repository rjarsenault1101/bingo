import json, random
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async

from init.models import Callable
from .models import CalledNumber

class CallConsumer(WebsocketConsumer):
    def connect(self):
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            "numbercalling", self.channel_name
        )
        
        self.accept()
        # This stuff probably needs to be another channel
        # already_called = list(CalledNumber.objects.all().values_list('number', flat=True))
        # already_called = [str(i) for i in already_called]
        # already_called = "  ".join(already_called)
        # async_to_sync(self.channel_layer.group_send)(
        #     "numbercalling",
        #     {
        #         'type': 'caller_number',
        #         'number': already_called
        #     }
        # )


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            "numbercalling", self.channel_name
        )

    # This gets called by the caller's new number button
    def receive(self, text_data):
        called = CalledNumber.objects.all().values_list('number', flat=True)
        callable_items = Callable.objects.values('value').exclude(value__in=called).values_list('value', flat=True)
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

# This one is for when someone calls bingo. Maybe also when they connect? Receive their name/team/cardID?
class BingoConsumer(WebsocketConsumer):
    def connect(self):
        name = self.scope['query_string'].decode("utf-8")
        # print(self.scope['path'])
        # print("query: " + name)
        async_to_sync(self.channel_layer.group_add)(
            "bingo", self.channel_name
        )
        
        self.accept()
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            "bingo", self.channel_name
        )
    def receive(self, text_data):
        # Stick this in a database table?
        async_to_sync(self.channel_layer.group_send)(
            "bingo", {
                'type': 'bingo',
                'info': text_data
            }
        )
    def bingo(self, event):
        data=json.loads(event['info'])
        print(data)
        self.send(text_data=json.dumps({
                    'bingo_alert': f"{data['name']} of the {data['team']} team called bingo!"
                }))
