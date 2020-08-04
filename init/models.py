from django.db import models

# Create your models here.
class Callable(models.Model):
    value = models.CharField(max_length=50)

class Info(models.Model):
    logged_in = models.IntegerField()

class WasActive(models.Model):
    username = models.CharField(max_length=50)
    team = models.CharField(max_length=50)
    duration = models.IntegerField()