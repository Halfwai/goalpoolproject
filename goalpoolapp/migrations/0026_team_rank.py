# Generated by Django 4.0.1 on 2022-11-07 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goalpoolapp', '0025_globalvars_remove_league_roundnumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='rank',
            field=models.IntegerField(default=1),
        ),
    ]