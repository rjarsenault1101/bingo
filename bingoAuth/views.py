from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from init.models import Team
from django.utils.datastructures import MultiValueDictKeyError

import logging

logger = logging.getLogger('bingo')
logger.setLevel(logging.INFO)


def login(request):
    if request.method == 'POST':
        try:
            username = request.POST['fname'] + " " + request.POST['lname']
            username = username.title()
            team = "no team" if "no" in request.POST['team'] else request.POST['team']
            leader = request.POST['leader']
            student_id = request.POST['studentid']
        except MultiValueDictKeyError:

            context = {
                'messages': ['A field was not filled out. Please try again.'],
                'teams': list(Team.objects.all().values_list('team', flat=True))

            }
            return render(request, 'registration/login.html', context=context)
        if not student_id.isdigit() or int(student_id) < 100000 or int(student_id) > 999999:
            context = {
                'firstname': request.POST['fname'],
                'lastname': request.POST['lname'],
                'leader': leader,
                'team': team,
                'messages': [
                    'invalid Student id',
                ],
                'teams': list(Team.objects.all().values_list('team', flat=True))
            }
            return render(request, 'registration/login.html', context=context)
        user = None
        try:

            user = User.objects.get(
                username=username, email=team, last_name=student_id)
        except User.DoesNotExist:
            pass

        if user is None:
            user = User(username=username, first_name="leader" in leader,
                        email=team, last_name=student_id)
            user.save()
        auth.login(request, user)
        logger.info(f"{username} of {team} just logged in")
        return redirect('index')
    return render(request, 'registration/login.html', context={'teams': list(Team.objects.all().values_list('team', flat=True))})
