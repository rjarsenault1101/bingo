# Generated by Django 3.0.8 on 2020-07-22 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('init', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.CharField(max_length=50)),
            ],
        ),
    ]