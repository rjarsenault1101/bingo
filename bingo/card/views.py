from django.shortcuts import render, redirect
import random
from .models import Card, CardUser
from caller.models import CalledNumber
from django.contrib.auth.models import User
# Create your views here.
def index(request):
    user = User.objects.get(pk=request.user.id)
    called = get_called()
    if CardUser.objects.filter(user_id=user.id).exists():
        # User has a card. send context containing card's numbers transposed
        card_user = CardUser.objects.get(user_id=user.id)
        card = Card.objects.get(id=card_user.card_id)
        numbers = card.b + card.i + card.n + card.g + card.o
        numbers = transpose(numbers)
    else:
        # No card exists for this user. Generate one
        numbers, card = generate_card()
        card_user = CardUser(card_id=card.id, user_id=user.id)
        card_user.save()
    context = {
        'called': called,
        'card_id': card.id,
        'numbers': numbers, 
        'user': user
    }

    return render(request, 'index.html', context)

def get_called():
    called = list(CalledNumber.objects.all().values_list('number', flat=True))
    return "  ".join([str(i) for i in called]) + "  "

def generate_card(): 
    b = random.sample(range(1,16), 5)
    i = random.sample(range(16,31), 5)
    n = random.sample(range(31,46), 5)
    g = random.sample(range(46,61), 5)
    o = random.sample(range(61,76), 5)
    numbers = b + i + n + g + o 
    numbers[12]="FREE"
    card = Card(b=b, i=i, n=n, g=g, o=o)
    card.save()
    numbers = transpose(numbers)
    return [numbers, card]

def transpose(list):
    new_list = []
    for i in range(5):
        new_list.append(list[i])
        new_list.append(list[i+5])
        new_list.append(list[i+10])
        new_list.append(list[i+15])
        new_list.append(list[i+20])
    return new_list