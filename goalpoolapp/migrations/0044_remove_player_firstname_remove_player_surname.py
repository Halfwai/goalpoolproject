# Generated by Django 4.0.1 on 2022-11-17 03:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goalpoolapp', '0043_player_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='player',
            name='surname',
        ),
    ]