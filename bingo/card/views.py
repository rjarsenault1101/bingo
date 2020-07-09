from django.shortcuts import render, redirect
import random
from .models import Card

# Create your views here.
def index(request):
    if request.session.get('numbers', None) != None:
        context = {
            'numbers': request.session['numbers']
        }
    else:
        numbers = generate_card()[0]
        context = {
            'card_id': id,
            'numbers': list(numbers)
        }
    request.session['numbers'] = context['numbers']
    return render(request, 'index.html', context)

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
    context = {
        'card_id': id,
        'numbers': list(numbers)
    }
    request.session['numbers'] = context['numbers']
    return redirect('index')