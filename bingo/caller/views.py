from django.shortcuts import render
from init.models import Callable
from .models import CalledNumber

# Create your views here.
def caller(request): 
    return render(request, 'caller.html')

def new_number(request):
    # put a new number that hasn't been called into the database
    # Get what's been called, get what can be called
    # Subtract what's been called from what can be called
    # Pick a random element from that remaining list
    callable_items = Callable.objects.values('value').exclude(value__in=CalledNumber.objects.all().values_list('number', flat=True)).all().values_list('value', flat=True)
    print(callable_items)
    return render(request, 'caller.html')

def clear_calls(request):
    # This goes and deletes all from the called database
    pass