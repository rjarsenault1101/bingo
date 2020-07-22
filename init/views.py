from django.shortcuts import render
from .models import Callable
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def index(request):
    if request.method == 'POST': 
        teams = request.POST['teamsbox'];
        print(teams)
        return render(request, 'caller.html')
    return render(request, 'init.html')

# Create your views here.
def numbers(request):
    callable = list(Callable.objects.all().values_list('value', flat=True))
    callable = [int(i) for i in callable]
    callable.sort()
    return JsonResponse(callable, safe=False)