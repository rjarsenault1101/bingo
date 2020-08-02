from django.db import models

# Create your models here.
class Callable(models.Model):
    value = models.CharField(max_length=50)

class Info(models.Model):
    logged_in = models.IntegerField()