from django.shortcuts import render
from init.models import Callable
from .models import CalledNumber
import random
# Create your views here.
def caller(request): 
    called = CalledNumber.objects.all().values_list('number', flat=True)
    called = "  ".join([str(i) for i in called]) + "  " 

    return render(request, 'caller.html', {
        'called': called
    })

def new_number(request):
    # Get what's been called, get what can be called
    # Subtract what's been called from what can be called
    # Pick a random element from that remaining list
    callable_items = list(Callable.objects.values('value').exclude(value__in=CalledNumber.objects.all().values_list('number', flat=True)).values_list('value', flat=True))
    new_number = CalledNumber(number=int(random.choice(callable_items)))
    new_number.save()
    
    return render(request, 'caller.html')

def clear_calls(request):
    # This goes and deletes all from the called database
    CalledNumber.objects.all().delete()
    return render(request, 'caller.html')