from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    name = models.CharField(max_length=50)
    team = models.CharField(max_length=50)
    # card = models.ForeignKey(
    #     'card.Card', on_delete=models.CASCADE
    # )