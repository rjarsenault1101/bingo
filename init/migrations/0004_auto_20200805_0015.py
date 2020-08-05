# Generated by Django 3.0.8 on 2020-08-05 00:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('init', '0003_wasactive'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wasactive',
            name='team',
        ),
        migrations.RemoveField(
            model_name='wasactive',
            name='username',
        ),
        migrations.AddField(
            model_name='wasactive',
            name='bingos',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='wasactive',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='wasactive',
            name='duration',
            field=models.IntegerField(default=0),
        ),
    ]