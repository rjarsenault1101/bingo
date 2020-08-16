import json
import logging
import random

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User

from init.models import Callable, WasActive

from .models import CalledNumber

logger = logging.getLogger('bingo')
logger.setLevel(logging.INFO)


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
            callable_items = Callable.objects.values('value').exclude(
                value__in=called).values_list('value', flat=True)
            callable_items = list(callable_items)
            new_number = CalledNumber(
                number=int(random.choice(callable_items)))
            new_number.save()
            logger.info(f"New number {new_number} has been called")
            async_to_sync(self.channel_layer.group_send)(
                "numbercalling",
                {
                    'type': 'call_number',
                    'number': new_number.number
                }
            )
        if data['type'] == 'reset':
            CalledNumber.objects.all().delete()
            logger.info("Resetting the game")
            async_to_sync(self.channel_layer.group_send)(
                "numbercalling",
                {
                    'type': 'reset'
                }
            )
        if data['type'] == 'accept':
            name = data['name']
            team = data['team']
            user = User.objects.get(username=name, email=team)
            activity = WasActive.objects.get(user_id=user)
            activity.bingos += 1
            logger.info(f"Bingo from {name}, {team} has been accepted")
            activity.save()

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
        self.accept()

    def disconnect(self, code):
        super()
        async_to_sync(self.channel_layer.group_discard)(
            "bingo", self.channel_name
        )

    def receive(self, text_data):
        text_data = json.loads(text_data)
        if text_data['type'] == 'bingo':
            logger.info(f"{text_data['name']} of {text_data['team']} called bingo")
            async_to_sync(self.channel_layer.group_send)(
                "bingo", {
                    'type': 'bingo',
                    'name': text_data['name'],
                    'team': text_data['team'],
                    'card_id': text_data['card_id'],
                    'leader': text_data['leader'] == 'True'
                }
            )

    def bingo(self, event):
        self.send(text_data=json.dumps({
            'type': 'bingo',
            'bingo_alert': f"[{event['card_id']}] - {'leader/volunteer ' if event['leader'] else ''} {event['name']} {'of {}'.format(event['team']) if 'no' not in event['team'] else ''} called bingo!",
            'name': event['name'],
            'team': event['team'],
            'card_id': event['card_id'],
        }))
