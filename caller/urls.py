from django.urls import path

from . import views

urlpatterns = [
    path('', views.caller, name="caller"),
    path('reset', views.reset, name='reset'),
    path('teams', views.get_teams_info, name='teams'),
]
