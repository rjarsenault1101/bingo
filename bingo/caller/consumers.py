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
        async_to_sync(self.channel_layer.group_add)(
            "bingo", self.channel_name
        )
        async_to_sync(self.channel_layer.group_add)(
            "login", self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # logout - remove name, team, card
        async_to_sync(self.channel_layer.group_send)(
            "login", {
                'type': 'logout'
                # 'name': text_data['name'],
                # 'team': text_data['team'],
                # 'card': text_data['card_id']
            }
        )
        async_to_sync(self.channel_layer.group_discard)(
            "bingo", self.channel_name
        )
        async_to_sync(self.channel_layer.group_discard)(
            "login", self.channel_name
        )
    def receive(self, text_data):
        text_data = json.loads(text_data)
        if text_data['type'] == 'bingo':
            async_to_sync(self.channel_layer.group_send)(
                "bingo", {
                    'type': 'bingo',
                    'name': text_data['name'],
                    'team': text_data['team'],
                    'card': text_data['card_id']
                }
            )
        if text_data['type'] == 'login':
            async_to_sync(self.channel_layer.group_send)(
                "login", {
                    'type': 'login',
                    'name': text_data['name'],
                    'team': text_data['team'],
                    'card': text_data['card_id']
                }
            )
    def bingo(self, event):
        self.send(text_data=json.dumps({
                    'type': 'bingo',
                    'bingo_alert': f"{event['name']} of the {event['team']} team called bingo!"
                }))
    def login(self, event):
        self.send(text_data=json.dumps({
            'type': 'login',
            'name': event['name'],
            'team': event['team'],
            'card': event['card']
        }))
    def logout(self, event):
        self.send(text_data=json.dumps({
            'type': 'logout'
        }))
class LoginConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            "login", self.channel_name
        )
        # Login - send name, team, card
        self.accept()

    def login(self, event):
        self.send(text_data=json.dumps({
            'name': event['name'],
            'team': event['team'],
            'card': event['card']
        }))
        
    def disconnect(self, close_code):
        # logout - remove name, team, card
        async_to_sync(self.channel_layer.group_discard)(
            "login", self.channel_name
        )
    def receive(self, text_data):
        data = json.dumps(text_data)

        async_to_sync(self.channel_layer.group_send)(
            "login", {
                'type': 'login',
                'name': data['name'],
                'team': data['team'],
                'card': data['card']
            }
        )