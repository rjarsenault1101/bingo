from django.shortcuts import render, redirect
import random

# Create your views here.
def index(request):
    if request.session.get('numbers', None) != None:
        context = {
            'numbers': request.session['numbers']
        }
    else:
        context = {
            'numbers': generate_card()
        }
    request.session['numbers'] = context['numbers']
    return render(request, 'index.html', context)

def generate_card(): 
    b = [i for i in range(1,16)]
    i = [i for i in range(16,31)]
    n = [i for i in range(31,46)]
    g = [i for i in range(46,61)]
    o = [i for i in range(61,76)]
    list=[]
    for value in range(25): 
        if value % 5 == 0: 
            list.append(get_number(b))
        if value % 5 == 1: 
            list.append(get_number(i))
        if value % 5 == 2: 
            list.append(get_number(n))
        if value % 5 == 3: 
            list.append(get_number(g))
        if value % 5 == 4: 
            list.append(get_number(o))
        print(list[value])
    list[12]="FREE"
    return list

def get_number(number_list):
    number = random.choice(number_list)
    number_list.remove(number)
    return number


def new_card(request):
    context = {
            'numbers': generate_card()
    }
    request.session['numbers'] = context['numbers']
    return redirect('index')