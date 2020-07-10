from django.shortcuts import render, redirect
import random
from .models import Card
from caller.models import CalledNumber

# Create your views here.
def index(request):
    called = get_called()
    if request.session.get('numbers', None) != None:
        context = {
            'numbers': request.session['numbers'],
            'called': called
        }
    else:
        numbers = generate_card()[0]
        context = {
            'card_id': id,
            'numbers': list(numbers),
            'called': called
        }
    request.session['numbers'] = context['numbers']
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
    return [numbers, card.id]

def transpose(list):
    new_list = []
    for i in range(5):
        new_list.append(list[i])
        new_list.append(list[i+5])
        new_list.append(list[i+10])
        new_list.append(list[i+15])
        new_list.append(list[i+20])
    return new_list

def new_card(request):
    numbers, id = generate_card()
    called = get_called()
    context = {
        'card_id': id,
        'numbers': list(numbers),
        'called': called
    }
    request.session['numbers'] = context['numbers']
    return redirect('index')