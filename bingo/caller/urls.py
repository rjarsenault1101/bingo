from django.urls import path

from . import views 

urlpatterns = [
    path('', views.caller, name="caller"),
    path('newNumber', views.new_number, name="newNumber"),
    path('clear', views.clear_calls, name='clear'),
]