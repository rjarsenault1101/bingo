from django.db import models

# Create your models here.
class CalledNumber(models.Model):
    number = models.CharField(max_length=50)