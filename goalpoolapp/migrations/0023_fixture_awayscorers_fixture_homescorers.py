# Generated by Django 4.0.1 on 2022-11-05 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goalpoolapp', '0022_league_roundnumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='fixture',
            name='awayscorers',
            field=models.ManyToManyField(blank=True, related_name='awaygamesscoredin', to='goalpoolapp.Player'),
        ),
        migrations.AddField(
            model_name='fixture',
            name='homescorers',
            field=models.ManyToManyField(blank=True, related_name='homegamesscoredin', to='goalpoolapp.Player'),
        ),
    ]