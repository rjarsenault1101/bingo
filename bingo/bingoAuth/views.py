from django.shortcuts import render, redirect
import json
from django.contrib import auth
from django.contrib.auth.models import User

# Create your views here.
def login(request):
    if request.method == 'POST': 
        username = request.POST['name']
        team = request.POST['team']
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
    return render(request, 'registration/login.html')