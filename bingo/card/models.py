from django.db import models
from django_mysql.models import ListTextField
# Create your models here.
class Card(models.Model):
    b = ListTextField(base_field=models.IntegerField())
    i = ListTextField(base_field=models.IntegerField())
    n = ListTextField(base_field=models.IntegerField())
    g = ListTextField(base_field=models.IntegerField())
    o = ListTextField(base_field=models.IntegerField())
