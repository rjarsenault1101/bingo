# Generated by Django 3.0.8 on 2020-07-11 00:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0001_initial'),
        ('bingoAuth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='card',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='card.Card'),
            preserve_default=False,
        ),
    ]
