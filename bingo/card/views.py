from django.shortcuts import render
import random

# Create your views here.
def index(request):
    context = {
        'numbers': generateNumbers()
    }
    return render(request, 'index.html', context)

def generateNumbers(): 
    list= random.sample(range(1, 100), 25)
    list[12]="FREE"
    return list