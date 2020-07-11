from django.shortcuts import render, redirect
import json
from .models import User
# Create your views here.
def login(request):
    if request.method == 'GET': 
        if request.session.get('name', None) == None:
            return render(request, 'registration/login.html')
        return redirect('index')
    else: 
        request.session['name'] = request.POST['name']
        request.session['team'] = request.POST['team']
        user = User(name=request.POST['name'], team=request.POST['team'])
        user.save()
        return redirect('index')