from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Callable, Team, Info
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def init(request):
    # Get the teams, get the values, name and card header to populate
    callable_values = list(Callable.objects.all().values_list('value', flat=True))
    callable_values = ", ".join(callable_values)

    teams = list(Team.objects.all().values_list('team', flat=True))
    teams = ", ".join(teams)
    context = {
        'values': callable_values,
        'teams': teams, 
    }

    if request.method == 'POST':
        Team.objects.all().delete()
        Callable.objects.all().delete()
        Info.objects.all().delete()

        if request.POST.get('teams'):
            teams = request.POST['teamsbox'].split(",")
            for team in teams:
                db_team = Team(team=team.strip())
                db_team.save()

        if request.POST['bingo'] == 'custom':
            callable_values = request.POST['customvalues'].split(',')
            for value in callable_values:
                db_value = Callable(value=value.strip())
                db_value.save()
        else: 
            for value in range(1, 76):
                Callable(value=value).save()

        if 'name' in request.POST:
            group_name = request.POST['name']

        if 'cardheader' in request.POST:
            card_header = request.POST['cardheader']
            
        Info(
            card_name=card_header if card_header else "bingo",
            group_name=group_name if group_name else "Bingo!",
            card_rows=request.POST['cardrows']
        ).save()

        return redirect('index')
    return render(request, 'init.html', context)

# Create your views here.
def numbers(request):
    callable_values = list(Callable.objects.all().values_list('value', flat=True))
    callable_values = [int(i) for i in callable_values]
    callable_values.sort()
    return JsonResponse(callable_values, safe=False)
