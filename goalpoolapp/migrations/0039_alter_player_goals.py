# Generated by Django 4.0.1 on 2022-11-14 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goalpoolapp', '0038_alter_player_leagues'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='goals',
            field=models.IntegerField(default=0),
        ),
    ]
