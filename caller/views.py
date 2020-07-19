from django.shortcuts import render
from init.models import Callable
from .models import CalledNumber

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
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

@staff_member_required
def clear_calls(request):
    # This goes and deletes all from the called database
    CalledNumber.objects.all().delete()
    return render(request, 'caller.html')