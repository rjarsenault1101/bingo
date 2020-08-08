from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from init.models import Team

def login(request):
    if request.method == 'POST':
        username = request.POST['fname'] + " " + request.POST['lname']
        username = username.title()
        team = request.POST['team']
        user = None
        try:
            user = User.objects.get(username=username, email=team)
        except User.DoesNotExist:
            pass

        if user is None:
            user = User(username=username, email=team, last_name=0)
            user.save()
        auth.login(request, user)
        return redirect('index')
    elif request.method == 'GET':
        teams = list(Team.objects.all().values_list('team', flat=True))
        return render(request, 'registration/login.html', context={'teams': teams})
