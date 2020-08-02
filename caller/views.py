from django.http import JsonResponse
from django.shortcuts import render
from init.models import Callable
from .models import CalledNumber
from django.contrib.auth.models import User
import json
from django.contrib.admin.views.decorators import staff_member_required

import logging
logger = logging.getLogger('bingo')
logger.setLevel(logging.INFO)


@staff_member_required
def caller(request):
    called = list(CalledNumber.objects.all().values_list('number', flat=True))
    numbers = list(Callable.objects.all().values_list('value', flat=True))
    numbers = [int(i) for i in numbers]
    called = [int(i) for i in called]
    numbers.sort()
    users = User.objects.filter(first_name="True").exclude(
        is_staff=True).count()
    return render(request, 'caller.html', {
        'called': called,
        'numbers': numbers,
        'col_count': len(numbers)/5,
        'users': users
    })


@staff_member_required
def clear_calls(request):
    # This goes and deletes all from the called database
    CalledNumber.objects.all().delete()
    return render(request, 'caller.html')


@staff_member_required
def get_active_users(request):
    users = User.objects.filter(first_name="True").exclude(
        is_staff=True).order_by('email')
    users = list(users)
    logger.info(users)
    values = []
    for user in users:
        values.append({
            'username': user.username,
            'team': user.email
        })
    values = json.dumps({
        'users': values
    })
    return JsonResponse(values, safe=False)
