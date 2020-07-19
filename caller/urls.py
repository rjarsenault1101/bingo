from django.urls import path

from . import views 

urlpatterns = [
    path('', views.caller, name="caller"),
    path('clear', views.clear_calls, name='clear'),
]