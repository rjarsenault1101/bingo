from django.urls import path

from . import views

urlpatterns = [
    path('', views.caller, name="caller"),
    path('reset', views.reset, name='reset'),
    path('users', views.get_active_users, name='users'),
    path('teams', views.get_teams_info, name='teams'),
]
