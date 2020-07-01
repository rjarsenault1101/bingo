from django.shortcuts import render
import random

# Create your views here.
def index(request):
    if request.session.get('numbers', None) != None:
        context = {
            'numbers': request.session['numbers']
        }
    else:
        context = {
            'numbers': generateNumbers()
        }
    request.session['numbers'] = context['numbers']
    return render(request, 'index.html', context)

def generateNumbers(): 
    list= random.sample(range(1, 100), 25)
    list[12]="FREE"
    return list