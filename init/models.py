from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Callable(models.Model):
    value = models.CharField(max_length=50)


class Info(models.Model):
    logged_in = models.IntegerField()


class WasActive(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    duration = models.IntegerField(default=0)
    bingos = models.IntegerField(default=0)
