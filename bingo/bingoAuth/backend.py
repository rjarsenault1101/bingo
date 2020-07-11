from django.contrib.auth.backends import BaseBackend
from .models import User

class BingoBackend(BaseBackend):
    def authenticate(self, request, username=None, team=None):
        try:
            user = User.objects.get(name=username, team=team)
            return user
        except User.DoesNotExist:
            user = User(name=username, team=team)
            user.save()
            return user
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        