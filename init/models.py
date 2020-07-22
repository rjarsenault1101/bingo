from django.db import models

# Create your models here.
class Callable(models.Model):
    value = models.CharField(max_length=50)

class Team(models.Model):
    value = models.CharField(max_length=50)