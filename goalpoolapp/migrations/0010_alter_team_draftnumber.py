# Generated by Django 4.0.1 on 2022-10-31 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goalpoolapp', '0009_league_draftposition_team_draftnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='draftNumber',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
