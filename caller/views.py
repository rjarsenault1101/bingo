import json
import logging

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from card.models import CardUser
from init.models import Callable, WasActive

from .models import CalledNumber

logger = logging.getLogger('bingo')
logger.setLevel(logging.INFO)


@staff_member_required
def caller(request):
    called = list(CalledNumber.objects.all().values_list('number', flat=True))
    numbers = list(Callable.objects.all().values_list('value', flat=True))
    numbers = [int(i) for i in numbers]
    called = [int(i) for i in called]
    numbers.sort()
    logger.info("Loading caller view")
    return render(request, 'caller.html', {
        'called': called,
        'numbers': numbers,
        'col_count': len(numbers)/5,
    })


@staff_member_required
def reset(request):
    # This goes and deletes all from the called database
    CalledNumber.objects.all().delete()
    WasActive.objects.all().delete()
    CardUser.objects.all().delete()
    User.objects.all().filter(is_staff=False).delete()
    logger.info("Resetting everything. Good bye!")
    return render(request, 'caller.html')


@staff_member_required
def get_teams_info(request):
    user_total = list(WasActive.objects.all())
    teams = dict()
    for user in user_total:
        if user.user.email not in teams:
            teams[user.user.email] = dict()
            teams[user.user.email]['users'] = []
            teams[user.user.email]['count'] = 0
        teams[user.user.email]['users'].append({
            'name': f"{user.user.username} (id# {user.user.last_name})",
            'bingos': user.bingos,
            'duration': user.duration
        })
        teams[user.user.email]['count'] += user.bingos
    return render(request, '_modaltable.html', context={
        'teams': teams.items()
    })
