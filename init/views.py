from django.shortcuts import render
from .models import Callable
from django.http import JsonResponse
from .models import Callable, Team
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def index(request):
    # Get the teams, get the values, name and card header to populate
    callable = list(Callable.objects.all().values_list('value', flat=True))
    callable = ", ".join(callable)

    teams = list(Team.objects.all().values_list('team', flat=True))
    teams = ", ".join(callable)
    context = {
        'values': callable,
        'teams': teams, 
    }
    if request.method == 'POST': 
        teams = request.POST['teamsbox'];
        
        return render(request, 'caller.html')
    return render(request, 'init.html', context)

# Create your views here.
def numbers(request):
    callable = list(Callable.objects.all().values_list('value', flat=True))
    callable = [int(i) for i in callable]
    callable.sort()
    return JsonResponse(callable, safe=False)