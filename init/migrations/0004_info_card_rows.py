# Generated by Django 3.0.8 on 2020-07-24 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('init', '0003_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='card_rows',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
    ]
