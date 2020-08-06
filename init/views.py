from django.http import JsonResponse
from django.shortcuts import render

from .models import Callable


# Create your views here.
def numbers(request):
    callable = list(Callable.objects.all().values_list('value', flat=True))
    callable = [int(i) for i in callable]
    callable.sort()
    return JsonResponse(callable, safe=False)
