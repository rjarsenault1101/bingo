from django.db import models

# Create your models here.
class Callable(models.Model):
    value = models.CharField(max_length=50)

class Team(models.Model):
    team = models.CharField(max_length=50)

class Info(models.Model):
    card_name = models.CharField(max_length=10)
    group_name = models.CharField(max_length=20)
    card_rows = models.IntegerField()
