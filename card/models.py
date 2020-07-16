from django.db import models
from django_mysql.models import ListTextField
from django.contrib.auth.models import User
# Create your models here.
class Card(models.Model):
    b = ListTextField(base_field=models.CharField(max_length=50))
    i = ListTextField(base_field=models.CharField(max_length=50))
    n = ListTextField(base_field=models.CharField(max_length=50))
    g = ListTextField(base_field=models.CharField(max_length=50))
    o = ListTextField(base_field=models.CharField(max_length=50))

class CardUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)