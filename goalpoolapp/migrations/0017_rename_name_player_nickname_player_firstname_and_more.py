# Generated by Django 4.0.1 on 2022-11-01 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goalpoolapp', '0016_league_draftdecending'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='name',
            new_name='nickname',
        ),
        migrations.AddField(
            model_name='player',
            name='firstname',
            field=models.CharField(default='null', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='surname',
            field=models.CharField(default='null', max_length=64),
            preserve_default=False,
        ),
    ]
