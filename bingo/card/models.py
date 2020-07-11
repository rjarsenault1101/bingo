from django.db import models
from django_mysql.models import ListTextField
from django.contrib.auth.models import User
# Create your models here.
class Card(models.Model):
    b = ListTextField(base_field=models.IntegerField())
    i = ListTextField(base_field=models.IntegerField())
    n = ListTextField(base_field=models.IntegerField())
    g = ListTextField(base_field=models.IntegerField())
    o = ListTextField(base_field=models.IntegerField())

class CardUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)