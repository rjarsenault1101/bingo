from django.shortcuts import render
from init.models import Callable
from .models import CalledNumber
from card.models import CardUser
import random
# Create your views here.
def caller(request): 
    called = list(CalledNumber.objects.all().values_list('number', flat=True))
    numbers = list(Callable.objects.all().values_list('value', flat=True))
    numbers = [int(i) for i in numbers]
    called = [int(i) for i in called]
    numbers.sort()
    return render(request, 'caller.html', {
        'called': called,
        'numbers': numbers,
        'col_count': len(numbers)/5
    })

def clear_calls(request):
    # This goes and deletes all from the called database
    CalledNumber.objects.all().delete()
    return render(request, 'caller.html')