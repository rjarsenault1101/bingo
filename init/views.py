from django.shortcuts import render
from .models import Callable
from django.http import JsonResponse
# Create your views here.
def numbers(request):
    callable = list(Callable.objects.all().values_list('value', flat=True)).sort()
    print(callable)
    return JsonResponse(callable, safe=False)