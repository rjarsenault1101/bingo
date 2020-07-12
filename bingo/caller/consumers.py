import json, random
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from card.models import CardUser
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
        data = json.loads(text_data)
        if data['type'] == 'call':        
            called = CalledNumber.objects.all().values_list('number', flat=True)
            callable_items = Callable.objects.values('value').exclude(value__in=called).values_list('value', flat=True)
            callable_items = list(callable_items)
            new_number = CalledNumber(number=int(random.choice(callable_items)))
            new_number.save()
            async_to_sync(self.channel_layer.group_send)(
                "numbercalling",
                {
                    'type': 'call_number',
                    'number': new_number.number
                }
            )
        if data['type'] == 'reset': 
            CalledNumber.objects.all().delete()
            async_to_sync(self.channel_layer.group_send)(
                "numbercalling",
                {
                    'type': 'reset'
                }
            )
    def reset(self, event):
        self.send(text_data=json.dumps({
            'type': 'reset'
        }))

    # Push new number to everyone
    def call_number(self, event):
        newNumber = event['number']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'call_number',
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
        user = self.scope['user']
        card_user = CardUser.objects.get(user_id=user.id)
        # logout - remove name, team, card
        async_to_sync(self.channel_layer.group_send)(
            "login", {
                'type': 'logout',
                'name': user.username,
                'team': user.email,
                'card': card_user.card_id
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
                    'bingo_alert': f"{event['name']} of the {event['team']} team called bingo!",
                    'small_alert': f"Someone from the {event['team']} team has just called bingo!"
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
            'type': 'logout',
            'name': event['name'],
            'team': event['team'],
            'card': event['card']
        }))