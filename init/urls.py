from django.urls import path

from . import views 

urlpatterns = [
    path('numbers', views.numbers, name='numbers'),
    path('', views.init, name='init'),
]