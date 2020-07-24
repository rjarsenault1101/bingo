from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from init.models import Team


def login(request):
    teams = list(Team.objects.all().values_list('team', flat=True))
    if request.method == 'POST': 
        username = request.POST['name']
        team = request.POST.get('team')
        team = team if team else "team"
        user = None
        try:
            user = User.objects.get(username=username, email=team)
        except User.DoesNotExist:
            pass

        if user is None:
            user = User(username=username, email=team)
            user.save()
        auth.login(request, user)
        return redirect('index')
    return render(request, 'registration/login.html', context={'teams': teams})